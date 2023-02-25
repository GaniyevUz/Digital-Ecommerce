from rest_framework.fields import (HiddenField, CurrentUserDefault, MultipleChoiceField, CharField,
                                   SerializerMethodField)
from rest_framework.serializers import ModelSerializer

from orders.models import Order
from shops.models import Shop, Category, Currency, PaymentProvider, TelegramBot


class ShopSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    languages = MultipleChoiceField(choices=Shop.Languages.choices)
    shop_orders_count = SerializerMethodField()
    shop_clients_count = SerializerMethodField()
    status = SerializerMethodField()
    shop_status_readable = SerializerMethodField()

    class Meta:
        model = Shop
        fields = '__all__'

    @staticmethod
    def get_shop_orders_count(obj: Shop):
        return obj.orders.count()

    @staticmethod
    def get_shop_clients_count(obj: Shop):
        return obj.clients.count()

    @staticmethod
    def get_status(obj: Shop):
        return ('inactive', 'active')[obj.is_active]

    @staticmethod
    def get_shop_status_readable(obj: Shop):
        return ('Inactive', 'Active')[obj.is_active]


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
        model = PaymentProvider
        exclude = ('shop',)


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = 'name',


class TelegramBotModelSerializer(ModelSerializer):
    shop = HiddenField(default=None)
    username = CharField(max_length=255, read_only=True)

    class Meta:
        model = TelegramBot
        fields = '__all__'
