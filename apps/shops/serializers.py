from rest_framework.fields import HiddenField, CurrentUserDefault, MultipleChoiceField
from rest_framework.serializers import ModelSerializer

from shops.models import Shop


class ShopSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    languages = MultipleChoiceField(choices=Shop.Languages.choices)

    class Meta:
        model = Shop
        fields = '__all__'
