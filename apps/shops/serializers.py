from rest_framework.serializers import ModelSerializer

from shops.models import Shop


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        exclude = ('user', )
