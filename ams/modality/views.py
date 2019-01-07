from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Modality, Team

from modality import serializers


class ModalityViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):
    """Manage modality in the database"""
    serializer_class = serializers.ModalitySerializer
    queryset = Modality.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the modality for the authenticated user"""
        return self.queryset.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ModalitySerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new modality"""
        serializer.save()


class TeamViewSet(viewsets.ModelViewSet):
    """Manage team in database"""
    serializer_class = serializers.TeamSerializer
    queryset = Team.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the modality for the authenticated user"""
        return self.queryset.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ModalitySerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new team"""
        serializer.save()
