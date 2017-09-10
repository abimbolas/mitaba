from django.contrib.auth.models import User
from mitaba.tracker.models import Entry
from rest_framework import serializers
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)


class EntrySerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'start', 'stop', 'details', 'owner')
        # only necessary in DRF3
        list_serializer_class = BulkListSerializer


class UserSerializer(serializers.ModelSerializer):
    # entry = serializers.PrimaryKeyRelatedField(many=True, queryset=Entry.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
