from rest_framework import serializers
from core.models import Sale, Transaction, Packet, User

#  Packet

from voucher.serializers import PacketSerializer
from product.serializers import TransactionSerializer


class SaleSerializer(serializers.ModelSerializer):
    """Serialize a sale"""

    vouchers = PacketSerializer(source='packet_set', many=True)
    products = TransactionSerializer(source='transaction_set', many=True)
    buyer = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all()
    )

    class Meta:
        model = Sale
        fields = (
            'id',
            'value',
            'date',
            'discount',
            'taxes',
            'vouchers',
            'products',
            'buyer'
        )
        read_only_fields = ('id', 'value', 'date')
        depth = 1

    def create(self, validated_data):
        value = 0.0
        vouchers = validated_data.pop('packet_set')
        products = validated_data.pop('transaction_set')
        sale = Sale.objects.create(**validated_data)

        for product in products:
            Transaction.objects.create(sale=sale, **product)
            value += (product['product'].price * product['amount'])

        for voucher in vouchers:
            Packet.objects.create(sale=sale, **voucher)
            value += (voucher['voucher'].price * voucher['amount'])

        sale.value = (value + (
            value * (validated_data['taxes'] / 100)
        ) - (
            value * (validated_data['discount'] / 100))
        )
        sale.save()

        return sale
