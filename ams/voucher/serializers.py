from rest_framework import serializers
from core.models import Voucher, Event, Packet


class VoucherSerializer(serializers.ModelSerializer):
    """Serializer a voucher"""

    event = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Event.objects.all()
    )

    class Meta:
        model = Voucher
        fields = ('id', 'price', 'amount', 'lot', 'event')
        read_only_fields = ('id',)


class PacketSerializer(serializers.ModelSerializer):
    """Serializer a packet"""

    class Meta:
        model = Packet
        fields = ('amount', 'voucher')

    def validate(self, data):
        """Check if the amount is avaliable"""
        tAmount = 0
        amounts = Packet.objects.all().values_list(
            'amount'
        ).filter(
            voucher=data['voucher'].id
        )

        for amount in amounts:
            for i in amount:
                tAmount += i

        tAmount += data['amount']

        if data['voucher'].amount < tAmount or data['amount'] <= 0:
            raise serializers.ValidationError("Ticket amount not avaliable")
        return data
