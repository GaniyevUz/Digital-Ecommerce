from rest_framework.fields import HiddenField, CurrentUserDefault, MultipleChoiceField, CharField
from rest_framework.serializers import ModelSerializer

from orders.models import Order
from shared.validators import telegram_bot
from shops.models import Shop, Category, Currency, PaymentProvider, TelegramBot


class ShopSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    languages = MultipleChoiceField(choices=Shop.Languages.choices)

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
        model = PaymentProvider
        fields = '__all__'


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

    def validate(self, attrs):
        return super().validate(attrs)

    def update(self, instance, validated_data):
        if token := validated_data.get('token'):
            telegram_bot(token)
        return super().update(instance, validated_data)
