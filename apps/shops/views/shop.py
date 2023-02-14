from django.db.models import Count
from django.db.models.expressions import RawSQL
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.serializers import OrderModelSerializer
from products.serializers import CategoryModelSerializer, ProductModelSerializer
from shared.mixins import CountResultMixin
from shared.permisions import IsAuthenticatedOwner, IsShopOwner
from shops.models import Shop
from shops.models.shop_belongs import PaymentProvider
from shops.serializers import ShopSerializer, PaymentSerializers


class ShopModelViewSet(ModelViewSet, CountResultMixin):
    serializer_class = ShopSerializer
    permission_classes = IsAuthenticatedOwner,
    queryset = Shop.objects.all()

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return self.count_result_list(request, *args, **kwargs)

    @action(['GET'], True, 'order', 'order', serializer_class=OrderModelSerializer)
    def get_orders(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        return self.get_count_result_list(shop.orders)

    @action(['GET'], False)
    def shop_config(self, request):
        langs = (("🇺🇿", "O'zbekcha", "uz"), ("🇷🇺", "Русский", "ru"), ("🇺🇸", "English", "en"))
        data = {"languages": [{'icon': i, 'title': t, 'code': c} for i, t, c in langs]}
        return Response(data)

    @action(['GET'], True, 'stat/all', 'stat_all')
    def main_stat(self, request, pk=None):

        orders = Order.objects.filter(items__order__shop_id=pk).annotate(total_items=Count('items'))
        total_orders = sum(orders.values_list('total_items', flat=True))

        paid_orders = orders.filter(paid=True).annotate(total_items=Count('items'))
        paid_orders_cost = sum(paid_orders.values_list('total_items', flat=True))

        _ = Order.objects.values('id').annotate(summ=RawSQL("SELECT get_summ_all(%s)", (1,)),
                                                avg=RawSQL("SELECT get_avarage_price(%s)", (1,)))[0]
        revenue, avg = _['summ'], _['avg']
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


class PaymentProvidersListAPIView(ListAPIView):
    queryset = PaymentProvider.objects.all()
    serializer_class = PaymentSerializers
