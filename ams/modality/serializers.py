from rest_framework import serializers
from core.models import Modality


class ModalitySerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    class Meta:
        model = Modality
        fields = ('id', 'name', 'sex', 'fee')
        read_only_fields = ('id',)
