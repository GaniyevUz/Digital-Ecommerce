from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.paginate import CountResultPaginate
from shared.permisions import IsAuthenticatedOwner
from shops.models import Shop
from shops.models.shop_belongs import PaymentProvider
from shops.serializers import ShopSerializer, PaymentSerializers


class ShopModelViewSet(ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = IsAuthenticatedOwner,
    queryset = Shop.objects.all()
    pagination_class = CountResultPaginate

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

    @action(['GET'], False)
    def shop_config(self, request):
        langs = (("🇺🇿", "O'zbekcha", "uz"), ("🇷🇺", "Русский", "ru"), ("🇺🇸", "English", "en"))
        data = {"languages": [{'icon': i, 'title': t, 'code': c} for i, t, c in langs]}
        return Response(data)


class PaymentProvidersListAPIView(ListAPIView):
    queryset = PaymentProvider.objects.all()
    serializer_class = PaymentSerializers
