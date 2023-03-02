from django.db import ProgrammingError
from django.db.models import Count
from django.db.models.expressions import RawSQL
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSetMixin

from shared.django import BaseShopMixin
from orders.models import Order
from shared.restframework import CountResultPaginate, IsAdminOrReadOnly, IsShopOwner
from shared.utils import TelegramBotValidator


from shops.models import Currency, Category, TelegramBot, PaymentProvider
from shops.serializers import CategorySerializer, CurrencySerializer, PaymentSerializers, TelegramBotModelSerializer


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class CurrencyModelViewSet(ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class PaymentProvidersViewSet(BaseShopMixin, ModelViewSet):
    serializer_class = PaymentSerializers
    queryset = PaymentProvider.objects.all()
    permission_classes = (IsShopOwner,)
    pagination_class = CountResultPaginate

    def perform_create(self, serializer):
        serializer.save(shop=self.get_shop())


class TelegramBotModelViewSet(ModelViewSet):
    serializer_class = TelegramBotModelSerializer
    queryset = TelegramBot.objects.all()
    permission_classes = AllowAny,

    def update(self, request, *args, **kwargs):
        token = request.data.get('token')
        validate = TelegramBotValidator()
        bot = validate(token, **kwargs)
        if bot.get('data'):
            return Response(bot['data'], status=bot['status'])
        if not bot.get('shop'):
            return Response(bot, status=status.HTTP_400_BAD_REQUEST)
        shop = bot['shop']
        bot, _ = TelegramBot.objects.update_or_create(shop=shop, defaults=bot)
        serializer = TelegramBotModelSerializer(bot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class StatShop(GenericAPIView, ViewSetMixin):
    serializer_class = TelegramBotModelSerializer
    queryset = TelegramBot.objects.all()
    permission_classes = AllowAny,

    @action(['GET'], True, 'stat/all', 'stat_all')
    def main_stat(self, request, pk=None):
        orders = Order.objects.filter(items__order__shop_id=pk).annotate(total_items=Count('items'))
        total_orders = sum(orders.values_list('total_items', flat=True))

        paid_orders = orders.filter(paid=True).annotate(total_items=Count('items'))
        paid_orders_cost = sum(paid_orders.values_list('total_items', flat=True))
        try:
            _ = Order.objects.values('id').annotate(summ=RawSQL("SELECT get_summ_all(%s)", (1,)),
                                                    avg=RawSQL("SELECT get_avarage_price(%s)", (1,)))[0]
            revenue, avg = _['summ'], _['avg']
        except ProgrammingError as error:
            revenue = avg = 0

        # total_customers = Client.objects.filter(shop_id=pk).count() # client chala
        data = {
            'id': pk,
            'total_orders': total_orders,
            'paid_orders': paid_orders_cost,
            'total_revenue': revenue,
            'total_customers': 'chala',
            'average_price': avg
        }
        return Response(data)
