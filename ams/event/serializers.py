from rest_framework import serializers
from core.models import Event, Modality
from modality.serializers import ModalitySerializer


class EventSerializer(serializers.ModelSerializer):
    """Serializer an event"""
    modalities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Modality.objects.all()
    )

    class Meta:
        model = Event
        fields = ('id', 'name', 'start', 'end', 'price', 'modalities')
        read_only_fields = ('id',)

    # def to_representation(self, instance):
    #     self.fields['modalities'] = ModalitySerializer(read_only=True)
    #     return super(EventSerializer, self).to_representation(instance)
