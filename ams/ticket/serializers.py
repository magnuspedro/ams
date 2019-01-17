from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """Serializer a ticket"""
    class Meta:
        model = Ticket
        fields = ('id', 'price', 'lot', 'date', 'delegation', 'event')
        read_only_fields = ('id',)


class TicketViewSerializer(serializers.ModelSerializer):
    """Serializer for only view"""
    class Meta:
        model = Ticket
        fields = (
            'id', 
            'code',
            'price', 
            'lot', 
            'status', 
            'date', 
            'delegation', 
            'event'
            )
        read_only_fields = ('id',)
