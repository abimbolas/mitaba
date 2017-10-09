from rest_framework.serializers import ModelSerializer
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer
from .models import Entry

class EntrySerializer(BulkSerializerMixin, ModelSerializer):
  class Meta(object):
    model = Entry
    exclude = ('user',)
    list_serializer_class = BulkListSerializer
