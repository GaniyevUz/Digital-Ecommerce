from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from io import BytesIO
from shared.utils import get_subdomain
from shops.models import Shop
from pandas import DataFrame, ExcelWriter


class BaseShopMixin:
    @property
    def get_shop(self):
        if shop_id := self.kwargs.get('shop'):  # noqa
            return get_object_or_404(Shop, pk=shop_id)
        if domain := get_subdomain(self.request):  # noqa
            return get_object_or_404(Shop, domain=domain)
        return None

    def get_queryset(self):
        queryset = self.queryset
        if hasattr(queryset.first, 'shop'):
            return queryset.filter(shop=self.get_shop)  # noqa


class APIViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ImportExportMixin:
    def export(self, *fields):
        if not fields:
            raise Exception(f'{self.__class__.__name__}.export required *fields')
        obj = self.get_queryset().first()
        for field in fields:
            if not hasattr(obj, field):
                raise Exception(f'{obj.__class__.__name__} has no field {field}')
        fields = list(fields)
        objects = self.get_queryset().values_list(*fields)
        data_frame = DataFrame(objects, columns=fields)
        with BytesIO() as export:
            data_frame.to_excel(export, 'products')
            return export.getvalue()
