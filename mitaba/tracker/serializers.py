from django.contrib.auth.models import User
from mitaba.tracker.models import Entry
from rest_framework import serializers


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Entry
        fields = ('id', 'start', 'stop', 'details', 'owner')


class UserSerializer(serializers.ModelSerializer):
    # entry = serializers.PrimaryKeyRelatedField(many=True, queryset=Entry.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
