from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Modality

from modality import serializers


class ModalityViewSet(viewsets.ModelViewSet):
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
