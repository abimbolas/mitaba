from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from .serializers import EntrySerializer
from .models import Entry

class EntryView(ListBulkCreateUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = EntrySerializer

    # Use only current user's own entries, with 'recent first' ordering
    def get_queryset(self):
      return Entry.objects.filter(user=self.request.user).order_by('-start')

    # Create new entries
    def perform_create(self, serializer):
      serializer.save(user=self.request.user)

    # DANGER: delete only entries listed in request
    def filter_queryset(self, queryset):
      filtered_queryset = queryset
      if self.request.method == 'DELETE':
        list_ids_of_entries = [e.get('id') for e in self.request.data]
        filtered_queryset = queryset.filter(pk__in=list_ids_of_entries)
      return filtered_queryset

