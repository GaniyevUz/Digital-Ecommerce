from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from products.models import Category
from products.serializers import CategoryMoveSerializer
from shared.django import APIViewSet
from shared.restframework import IsAuthenticatedOwner, CountResultPaginate
from shared.utils import site_languages
from shops.models import Shop, Country
from shops.models.shop_belongs import PaymentProvider
from shops.serializers import ShopSerializer, PaymentSerializers, CountrySerializer


class ShopAPIViewSet(APIViewSet):
    serializer_class = ShopSerializer
    permission_classes = IsAuthenticatedOwner,
    queryset = Shop.objects.all()
    pagination_class = CountResultPaginate
    lookup_url_kwarg = 'shop'

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        shop = serializer.save()
        user = self.request.user
        if not user.default_shop:
            user.default_shop = shop
            user.save()

    @action(['GET'], False)
    def shop_config(self, request):
        shop = self.request.user.default_shop
        languages = site_languages
        if shop:
            languages = list(filter(lambda _: _.get('code') in shop.languages, site_languages))
        data = {"languages": [_ for _ in languages]}
        return Response(data)


class CountryAPIViewSet(APIViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class PaymentProvidersListAPIView(ListAPIView):
    queryset = PaymentProvider.objects.all()
    serializer_class = PaymentSerializers