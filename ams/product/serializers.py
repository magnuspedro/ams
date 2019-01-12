from rest_framework import serializers
from core.models import Product, Event, Bought


class ProductSerializer(serializers.ModelSerializer):
    """Serialize a product"""
    event = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Event.objects.all()
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'amount',
                  'size', 'price', 'event')
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
