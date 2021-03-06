from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Sale

from sale import serializers


class SaleViewSet(viewsets.ModelViewSet):
    """Manage sale in the database"""
    serializer_class = serializers.SaleSerializer
    queryset = Sale.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retri the sale for the authenticade user"""
        return self.queryset.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.SaleSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new sale"""
        serializer.save(empl=self.request.user)
