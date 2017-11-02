from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import NotFound
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from .serializers import EntrySerializer
from .models import Entry
from mitaba.core.settings import log

class EntryView(ListBulkCreateUpdateDestroyAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	# renderer_classes = (JSONRenderer,)
	serializer_class = EntrySerializer
	# pagination_class = LimitOffsetPagination

	def list(self, request):

		# 'Last' query
		last = self.request.query_params.get('last', None)
		if last is not None:
			limit = int(self.request.query_params.get('limit', 1))
			offset = int(self.request.query_params.get('offset', 0))
			if limit < 1:
				raise ParseError(detail='Limit should be 1 or more')
			if offset < 0:
				raise ParseError(detail='Offset cannot be negative')
			group = None
			entries = None
			if last == 'days':
				entries, group = last_days_response(self.get_queryset(), limit, offset)
			elif last == 'months':
				entries, group = last_months_response(self.get_queryset(), limit, offset)
			elif last == 'years':
				entries, group = last_years_response(self.get_queryset(), limit, offset)
			else:
				raise NotFound()

			result_json = {'entries': self.get_serializer(entries, many=True).data}
			pagination_json = date_group_pagination(group, limit, offset, last)
			return Response({**result_json, **pagination_json})

		# Everything otherwise
		serializer = self.get_serializer(self.get_queryset(), many=True)
		return Response({ 'entries': serializer.data })

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

# Last days
def last_days_response(entries, limit, offset):
	group = entries.dates('start', 'day', order='DESC')
	if offset >= len(group):
		raise NotFound()
	lookup_days = group[offset:offset+limit]
	entries = entries.filter(start__date__in=lookup_days)
	if len(entries) == 0:
		raise NotFound()
	return (entries, group)

# Last months
def last_months_response(entries, limit, offset):
	group = entries.dates('start', 'month', order='DESC')
	if offset >= len(group):
		raise NotFound()
	lookup = group[offset:offset+limit]
	lookup_to = lookup[0] + relativedelta(months=+1)
	lookup_from = lookup[-1]
	entries = entries.filter(start__range=(lookup_from, lookup_to))
	if len(entries) == 0:
		raise NotFound()
	return (entries, group)

# Last years
def last_years_response(entries, limit, offset):
	group = entries.dates('start', 'year', order='DESC')
	if offset >= len(group):
		raise NotFound()
	lookup = group[offset:offset+limit]
	lookup_to = lookup[0] + relativedelta(years=+1)
	lookup_from = lookup[-1]
	entries = entries.filter(start__range=(lookup_from, lookup_to))
	if len(entries) == 0:
		raise NotFound()
	return (entries, group)

# Group pagination
def date_group_pagination(group, limit, offset, type):
	previous_group = None
	next_group = None
	if offset - limit >= 0:
		previous_group = list(map(lambda d: d.isoformat(), group[offset-limit:offset]))
		if len(previous_group) == 0:
			previous_group = None
	if offset + limit <= len(list(group)):
		next_group = list(map(lambda d: d.isoformat(), group[offset+limit:offset+limit+limit]))
		if len(next_group) == 0:
			next_group = None
	return {
		'pagination_group': {
			'previous': previous_group,
			'next': next_group,
			'count': len(list(group)),
			'limit': limit,
			'offset': offset,
			'group': type
		}
	}
