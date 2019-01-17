from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import Voucher

from voucher import serializers


class VoucherViewSet(viewsets.ModelViewSet):
    """Manage product in the database"""
    serializer_class = serializers.VoucherSerializer
    queryset = Voucher.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retri the product for the authenticade user"""
        return self.queryset.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.VoucherSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new voucher"""
        serializer.save()
