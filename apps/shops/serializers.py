from rest_framework.serializers import ModelSerializer

from shops.models import Shop, Category, Currency
from shops.models.shop_belongs import PaymentProviders


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class PaymentSerializers(ModelSerializer):
    class Meta:
        model = PaymentProviders
        fields = '__all__'
