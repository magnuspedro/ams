from rest_framework import serializers
from core.models import Event, Competition, Modality
from modality.serializers import ModalitySerializer


class EventSerializer(serializers.ModelSerializer):
    """Serializer an event"""
    class Meta:
        model = Event
        fields = ('id', 'name', 'start', 'end', 'price')
        read_only_fields = ('id',)


class CompetitionSerializer(serializers.ModelSerializer):
    """Serialize a competition"""
    events = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Event.objects.all()
    )
    modalities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Modality.objects.all()
    )

    class Meta:
        model = Competition
        fields = ('events', 'modalities')
        read_only_fields = ('id',)


class CompetitionDetailSerializer(CompetitionSerializer):
    events = EventSerializer(many=True, read_only=True)
    modalities = ModalitySerializer(many=True, read_only=True)
