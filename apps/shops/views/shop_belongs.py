from django.db import ProgrammingError
from django.db.models import Count
from django.db.models.expressions import RawSQL
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from orders.models import ProductOrder
from orders.models import Order
from shared.django import BaseShopMixin, APIViewSet
from shared.restframework import CountResultPaginate, IsAdminOrReadOnly, IsShopOwner
from shared.utils import bot_validator
from shops.models import Currency, Category, TelegramBot, PaymentProvider
from shops.serializers import CategorySerializer, CurrencySerializer, PaymentSerializers, TelegramBotModelSerializer
import datetime


class CategoryAPIViewSet(APIViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class CurrencyAPIViewSet(APIViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class PaymentProvidersViewSet(BaseShopMixin, APIViewSet):
    serializer_class = PaymentSerializers
    queryset = PaymentProvider.objects.all()
    permission_classes = (IsShopOwner,)
    pagination_class = CountResultPaginate

    def perform_create(self, serializer):
        serializer.save(shop=self.get_shop())


class TelegramBotAPIViewSet(APIViewSet):
    serializer_class = TelegramBotModelSerializer
    queryset = TelegramBot.objects.all()
    permission_classes = AllowAny,

    def update(self, request, *args, **kwargs):
        token = request.data.get('token')
        bot = bot_validator(token, **kwargs)
        if bot.get('data'):
            return Response(bot['data'], status=bot['status'])
        if not bot.get('shop'):
            return Response(bot, status=status.HTTP_400_BAD_REQUEST)
        shop = bot['shop']
        bot, _ = TelegramBot.objects.update_or_create(shop=shop, defaults=bot)
        serializer = TelegramBotModelSerializer(bot)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatShop(GenericViewSet, GenericAPIView):
    serializer_class = TelegramBotModelSerializer
    queryset = TelegramBot.objects.all()
    permission_classes = AllowAny,

    @action(['GET'], False, 'all', 'stat_all')
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('shop')
        orders = Order.objects.filter(items__order__shop_id=pk).annotate(total_items=Count('items'))
        total_orders = sum(orders.values_list('total_items', flat=True))

        paid_orders = orders.filter(paid=True).annotate(total_items=Count('items'))
        paid_orders_cost = sum(paid_orders.values_list('total_items', flat=True))
        try:
            _ = Order.objects.values('id').annotate(summ=RawSQL("SELECT get_summ_all(%s)", (pk,)),
                                                    avg=RawSQL("SELECT get_avarage_price(%s)", (pk,)))[0]
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

    @action(['GET'], False, 'sales', 'stat_sales')
    def main_stat1(self, request, shop):
        orders = ProductOrder.objects.values('pk', 'product__price', 'count', 'order__created_at').filter(
            order__shop_id=shop,
            order__paid=True)
        ex = {}
        for i in orders:
            _ = datetime.datetime(i.get('order__created_at').year, i.get('order__created_at').month, 1, 0, 0, 0)
            if ex.get(_):
                ex[_] += int(i.get('product__price')) * i.get('count')
            else:
                ex[_] = int(i.get('product__price')) * i.get('count')

        data = {'results': []}
        for k, v in ex.items():
            data.get('results').append({'month': k,
                                        'order_total_price': v})
        return Response(data)
