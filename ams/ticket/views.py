from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import Ticket

from ticket import serializers


class TicketViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    """Manage ticket in the database"""
    serializer_class = serializers.TicketSerializer
    queryset = Ticket.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Create a new ticket"""
        serializer.save()


class TicketView(viewsets.GenericViewSet, mixins.ListModelMixin):

    serializer_class = serializers.TicketViewSerializer
    queryset = Ticket.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrie the product for the authenticade user"""
        return self.queryset.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.TicketViewSerializer

        return self.serializer_class
