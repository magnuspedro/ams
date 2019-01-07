from rest_framework import serializers
from core.models import Modality, User, Team
from user.serializers import UserSerializer


class ModalitySerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    class Meta:
        model = Modality
        fields = ('id', 'name', 'sex', 'fee')
        read_only_fields = ('id',)


class TeamSerializer(serializers.ModelSerializer):
    """Serialize a team"""
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    modalities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Modality.objects.all()
    )

    class Meta:
        model = Team
        fields = ('users', 'modalities')


class TeamDetailSerializer(ModalitySerializer):
    users = UserSerializer(many=True, read_only=True)
    modalities = ModalitySerializer(many=True, read_only=True)
