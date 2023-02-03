from rest_framework.serializers import ModelSerializer

from orders.models import Order
from products.serializers import ProductModelSerializer


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        exclude = ('shop',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        items = instance.items.all()
        delivery_price = instance.shop.delivery_price or 0
        data['items'] = [ProductModelSerializer(i).data for i in items]
        data['delivery_price'] = delivery_price
        data['total_price'] = sum([item.price for item in items] + [delivery_price])
        return data
