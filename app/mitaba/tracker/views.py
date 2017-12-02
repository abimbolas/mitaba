from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as ParseDate
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import NotFound, ParseError
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from .serializers import EntrySerializer
from .models import Entry
from mitaba.core.settings import log
# Utils
from functools import reduce
import operator
import re
import datetime
from django.db.models import Q
from django.utils.encoding import uri_to_iri
import urllib

dateRegexp = re.compile('(\s|^)((\d{4})|(\d{1,2}\.\d{4})|(\d{1,2}\.\d{1,2}\.\d{4}))(\s|$)')

default_entries_limit = 20
default_days_limit = 7
default_months_limit = 1
default_years_limit = 1
default_tasks_limit = 3

class EntryView(ListBulkCreateUpdateDestroyAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	# renderer_classes = (JSONRenderer,)
	serializer_class = EntrySerializer
	# pagination_class = LimitOffsetPagination

	def list(self, request):
		entries = self.get_queryset()
		context_json = {}
		pagination_json = None

		# Limit check
		limit = self.request.query_params.get('limit', None)
		if (limit is not None) and (limit != 'false'):
			try:
				limit = int(limit)
			except ValueError:
				raise ParseError(detail='Bad limit')
			if limit < 1:
				raise ParseError(detail='Limit should be 1 or more')

		# Offset check
		try:
			offset = int(self.request.query_params.get('offset', 0))
		except ValueError:
			offset = 0
		if offset < 0:
			raise ParseError(detail='Offset cannot be negative')

		# Count set
		count = entries.count()

		# 'Context' query
		context = self.request.query_params.getlist('context[]', None)
		if len(context) > 0:
			context_filter = {}
			detail_index = 0
			for detail in context:
				context_filter['details__' + str(detail_index)] = context[detail_index]
				detail_index = detail_index + 1
			entries = entries.filter(**context_filter)
			count = entries.count()
			context_json = {'context': context}

		# 'From' and 'To' query
		start_from = self.request.query_params.get('start_from', None)
		start_to = self.request.query_params.get('start_to', None)
		if (start_from is not None) or (start_to is not None):
			entries, count = interval_entries(entries, start_from, start_to)
			pagination_json = interval_pagination(count)

		# 'Filter' query
		filters = self.request.query_params.getlist('filter[]', None)
		if len(filters) > 0:
			entries, count = filter_entries(entries, filters, context)

		# 'Last' query
		last = self.request.query_params.get('last', None)
		if last is not None:
			group = None
			if last == 'days':
				if limit is None:
					limit = default_days_limit
				entries, group = last_days(entries, limit, offset)
			elif last == 'months':
				if limit is None:
					limit = default_months_limit
				entries, group = last_months(entries, limit, offset)
			elif last == 'years':
				if limit is None:
					limit = default_years_limit
				entries, group = last_years(entries, limit, offset)
			elif last == 'tasks':
				if limit is None:
					limit = default_tasks_limit
				entries, group = last_tasks(entries, limit, offset, len(context))
			else:
				raise NotFound()
			pagination_json = group_pagination(group, limit, offset, last)

		# Simple paginate
		if pagination_json is None:
			entries = last_items(entries, limit, offset)
			pagination_json = entries_pagination(limit, offset, count)

		# Final result
		entries_json = {'entries': self.get_serializer(entries, many=True).data}
		response_json = {**entries_json, **pagination_json, **context_json}
		return Response(response_json)

	# Use only current user's own entries, with 'recent first' ordering
	def get_queryset(self):
		return Entry.objects.filter(user=self.request.user).order_by('-start')

	# Create new entries
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	# Used for DELETE
	def filter_queryset(self, queryset):
		filtered_queryset = queryset
		# DANGER: delete only entries listed in request
		if self.request.method == 'DELETE':
			list_ids_of_entries = [e.get('id') for e in self.request.data]
			filtered_queryset = queryset.filter(pk__in=list_ids_of_entries)
		return filtered_queryset

#
# Filtering entries
#

def context_detail_filter(offset, detail):
	df = {}
	df['details__' + str(offset) + '_100__icontains'] = detail
	return df

# Interval entries
def interval_entries(entries, start_from, start_to):
	filtered_entries = entries
	start_datetime = None
	stop_datetime = None

	try:
		if (start_from is not None) and (start_from != 'auto'):
			start_datetime = ParseDate(start_from)
			filtered_entries = filtered_entries.filter(start__gte=start_datetime)
		if (start_to is not None) and (start_to != 'auto'):
			stop_datetime = ParseDate(start_to)
			filtered_entries = filtered_entries.filter(start__lte=stop_datetime)
	except ValueError:
		raise ParseError(detail='Bad start_from or start_to query params')

	filtered_count = filtered_entries.count()
	return (filtered_entries, filtered_count)

# Filtered entries
def filter_entries(entries, filters, context=[]):
	filtered_entries = entries
	# Filter date
	filter_date = list(filter(lambda f: dateRegexp.match(f) is not None, filters))
	if len(filter_date) > 0:
		filter_date = list(reversed(filter_date[0].split('.')))
		if len(filter_date) == 1:
			filtered_entries = filtered_entries.filter(start__year=filter_date[0])
		elif len(filter_date) >= 2:
			filtered_entries = filtered_entries.filter(start__year=filter_date[0], start__month=filter_date[1])
		elif len(filter_date) == 3:
			filtered_entries = filtered_entries.filter(start__year=filter_date[0], start__month=filter_date[1], start__day=filter_date[2])
		else:
			raise ParseError(detail='Bad date filter')
	# Filter details
	filter_details = list(filter(lambda f: dateRegexp.match(f) is None, filters))
	if len(filter_details) > 0:
		query = reduce(operator.and_, (Q(**context_detail_filter(len(context), d)) for d in filter_details))
		filtered_entries = filtered_entries.filter(query)
	# Set final count
	filtered_count = filtered_entries.count()
	return (filtered_entries, filtered_count)

# Last items
def last_items(entries, limit, offset):
	if offset >= len(entries):
		raise NotFound()
	filtered_entries = entries
	if limit == 'false':
		filtered_entries = entries[offset:len(entries)]
	elif limit is None:
		filtered_entries = entries[offset:offset+default_entries_limit]
	else:
		filtered_entries = entries[offset:offset+limit]
	if len(filtered_entries) == 0:
		raise NotFound()
	return filtered_entries

# Last days
def last_days(entries, limit, offset):
	group = entries.dates('start', 'day', order='DESC')
	if offset >= len(group):
		raise NotFound()
	lookup = group
	if limit == 'false':
		lookup = group[offset:len(group)]
	else:
		lookup = group[offset:offset+limit]
	filtered_entries = entries.filter(start__date__in=lookup)
	if len(filtered_entries) == 0:
		raise NotFound()
	return (filtered_entries, group)

# Last months
def last_months(entries, limit, offset):
	group = entries.dates('start', 'month', order='DESC')
	if offset >= len(group):
		raise NotFound()
	lookup = group
	if limit == 'false':
		lookup = group[offset:len(group)]
	else:
		lookup = group[offset:offset+limit]
	lookup_to = lookup[0] + relativedelta(months=+1)
	lookup_from = lookup[-1]
	filtered_entries = entries.filter(start__range=(lookup_from, lookup_to))
	if len(filtered_entries) == 0:
		raise NotFound()
	return (filtered_entries, group)

# Last years
def last_years(entries, limit, offset):
	group = entries.dates('start', 'year', order='DESC')
	if offset >= len(group):
		raise NotFound()
	lookup = group
	if limit == 'false':
		lookup = group[offset:len(group)]
	else:
		lookup = group[offset:offset+limit]
	lookup_to = lookup[0] + relativedelta(years=+1)
	lookup_from = lookup[-1]
	filtered_entries = entries.filter(start__range=(lookup_from, lookup_to))
	if len(filtered_entries) == 0:
		raise NotFound()
	return (filtered_entries, group)

# Last tasks
def last_tasks(entries, limit, offset, context_length):
	group = []
	all_details = entries.filter(details__len__gt=context_length).values('details')
	details_list = list(map(lambda d: d.get('details')[context_length], all_details))
	for d in details_list:
		if d not in group:
			group.append(d)
	lookup = group
	if limit == 'false':
		lookup = group[offset:len(group)]
	else:
		lookup = group[offset:offset+limit]
	lookup_param = {}
	lookup_param['details__' + str(context_length) + '__in'] = lookup
	filtered_entries = entries.filter(**lookup_param)
	return (filtered_entries, group)

# Interval pagination
def interval_pagination(count):
	return {
		'pagination': {
			'count': count,
			'limit': None,
			'offset': 0
		}
	}

# Entries pagination
def entries_pagination(limit, offset, count):
	parsed_limit = limit
	if limit == 'false':
		parsed_limit = False
	if limit is None:
		parsed_limit = default_entries_limit
	return {
		'pagination': {
			'count': count,
			'limit': parsed_limit,
			'offset': offset
		}
	}

# Group pagination
def get_group_value(item):
	if isinstance(item, datetime.date):
		return item.isoformat()
	else:
		return item

def group_pagination(group, limit, offset, type):
	previous_group = None
	next_group = None
	if offset - limit >= 0:
		previous_group = list(map(lambda g: get_group_value(g), group[offset-limit:offset]))
	else:
		previous_group = list(map(lambda g: get_group_value(g), group[0:offset]))

	if offset + limit <= len(list(group)):
		next_group = list(map(lambda g: get_group_value(g), group[offset+limit:offset+limit+limit]))
	else:
		next_group = list(map(lambda g: get_group_value(g), group[offset+limit:len(group)]))

	if len(previous_group) == 0:
		previous_group = None
	if len(next_group) == 0:
		next_group = None

	return {
		'pagination': {
			'previous': previous_group,
			'next': next_group,
			'count': len(list(group)),
			'limit': limit,
			'offset': offset,
			'group': type
		}
	}
