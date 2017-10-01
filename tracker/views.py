from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_bulk import BulkModelViewSet

from core.filters import IsOwnerFilterBackend
from tracker.models import Entry
from tracker.serializers import EntrySerializer

User = get_user_model()


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'entries': reverse('entry-list', request=request, format=format)
    })


class EntryViewSet(BulkModelViewSet):
    """
    Bulk update enabled view
    """
    queryset = Entry.objects.all().order_by('id')
    serializer_class = EntrySerializer
    filter_backends = (IsOwnerFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
