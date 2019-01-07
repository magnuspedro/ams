from rest_framework import serializers
from core.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer an event"""
    class Meta:
        model = Event
        fields = ('id', 'name', 'start', 'end', 'price')
        read_only_fields = ('id',)
