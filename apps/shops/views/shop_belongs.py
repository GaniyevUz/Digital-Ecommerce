from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from shops.models import Currency, Category
from shops.models.shop_belongs import PaymentProviders
from shops.serializers import CategorySerializer, CurrencySerializer, PaymentSerializers


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]


class CurrencyModelViewSet(ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentProvidersViewSet(ModelViewSet):
    serializer_class = PaymentSerializers
    queryset = PaymentProviders.objects.all()
