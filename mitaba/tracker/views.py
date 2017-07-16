from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from mitaba.tracker.models import Entry
from mitaba.tracker.serializers import EntrySerializer, UserSerializer
from mitaba.tracker.filters import IsOwnerFilterBackend


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'entries': reverse('entry-list', request=request, format=format)
    })


class EntryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    queryset = Entry.objects.all().order_by('id')
    serializer_class = EntrySerializer
    filter_backends = (IsOwnerFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)
