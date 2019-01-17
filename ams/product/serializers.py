from rest_framework import serializers
from core.models import Product, Event, Bought, Transaction


class ProductSerializer(serializers.ModelSerializer):
    """Serialize a product"""
    event = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Event.objects.all()
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'amount',
            'color',
            'size',
            'price',
            'event')
        read_only_fields = ('id',)


class BoughtSerializer(serializers.ModelSerializer):
    """Serialize a product that was bought"""
    product = ProductSerializer()

    class Meta:
        model = Bought
        fields = ('id', 'price', 'product')
        read_only_fields = ('id',)

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        product = Product.objects.create(**product_data)
        bought = Bought.objects.create(product=product, **validated_data)
        return bought


class TransactionSerializer(serializers.ModelSerializer):
    """Serialize a transaction"""
    class Meta:
        model = Transaction
        fields = ('amount', 'product',)

    def validate(self, data):
        """Check if the amount is avaliable"""
        tAmount = 0
        amounts = Transaction.objects.all().values_list(
            'amount'
        ).filter(
            product=data['product'].id
        )

        for amount in amounts:
            for i in amount:
                tAmount += i

        tAmount += data['amount']

        if data['product'].amount < tAmount or data['amount'] <= 0:
            raise serializers.ValidationError("Product amount not avaliable")
        return data
