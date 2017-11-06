from dateutil.relativedelta import relativedelta
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

dateRegexp = re.compile('(\s|^)((\d{4})|(\d{1,2}\.\d{4})|(\d{1,2}\.\d{1,2}\.\d{4}))(\s|$)')

class EntryView(ListBulkCreateUpdateDestroyAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	# renderer_classes = (JSONRenderer,)
	serializer_class = EntrySerializer
	# pagination_class = LimitOffsetPagination

	def list(self, request):
		entries = self.get_queryset()
		context_json = {}
		pagination_json = {}

		# Limit and Offset check
		limit = int(self.request.query_params.get('limit', 20))
		offset = int(self.request.query_params.get('offset', 0))
		count = entries.count()
		if limit < 1:
			raise ParseError(detail='Limit should be 1 or more')
		if offset < 0:
			raise ParseError(detail='Offset cannot be negative')

		# 'Context' query
		context = self.request.query_params.get('context', None)
		if context is not None:
			# filter context entries and pass further
			context_json = {'context': context}

		# 'Filter' query
		filters = self.request.query_params.getlist('filter[]', None)
		if len(filters) > 0:
			entries, count = filter_entries(entries, filters)

		# 'Last' query
		last = self.request.query_params.get('last', None)
		if last is not None:
			group = None
			if last == 'days':
				entries, group = last_days(entries, limit, offset)
			elif last == 'months':
				entries, group = last_months(entries, limit, offset)
			elif last == 'years':
				entries, group = last_years(entries, limit, offset)
			else:
				raise NotFound()
			pagination_json = group_pagination(group, limit, offset, last)

		# Simple paginate otherwise
		if (context is None) and (last is None):
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

# Filtered entries
def filter_entries(entries, filters):
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
		query = reduce(operator.and_, (Q(details__icontains=d) for d in filter_details))
		filtered_entries = filtered_entries.filter(query)
	# Set final count
	filtered_count = filtered_entries.count()
	return (filtered_entries, filtered_count)

# Last items
def last_items(entries, limit, offset):
	if offset >= len(entries):
		raise NotFound()
	filtered_entries = entries[offset:offset+limit]
	if len(filtered_entries) == 0:
		raise NotFound()
	return filtered_entries

# Last days
def last_days(entries, limit, offset):
	group = entries.dates('start', 'day', order='DESC')
	if offset >= len(group):
		raise NotFound()
	lookup_days = group[offset:offset+limit]
	filtered_entries = entries.filter(start__date__in=lookup_days)
	if len(filtered_entries) == 0:
		raise NotFound()
	return (filtered_entries, group)

# Last months
def last_months(entries, limit, offset):
	group = entries.dates('start', 'month', order='DESC')
	if offset >= len(group):
		raise NotFound()
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
	lookup = group[offset:offset+limit]
	lookup_to = lookup[0] + relativedelta(years=+1)
	lookup_from = lookup[-1]
	filtered_entries = entries.filter(start__range=(lookup_from, lookup_to))
	if len(filtered_entries) == 0:
		raise NotFound()
	return (filtered_entries, group)

# Entries pagination
def entries_pagination(limit, offset, count):
	return {
		'pagination': {
			'count': count,
			'limit': limit,
			'offset': offset
		}
	}

# Group pagination
def group_pagination(group, limit, offset, type):
	previous_group = None
	next_group = None
	if offset - limit >= 0:
		previous_group = list(map(lambda d: d.isoformat(), group[offset-limit:offset]))
		if len(previous_group) == 0:
			previous_group = None
	else:
		previous_group = list(map(lambda d: d.isoformat(), group[0:offset]))
	if offset + limit <= len(list(group)):
		next_group = list(map(lambda d: d.isoformat(), group[offset+limit:offset+limit+limit]))
		if len(next_group) == 0:
			next_group = None
	else:
		next_group = list(map(lambda d: d.isoformat(), group[offset+limit:len(group)]))
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
