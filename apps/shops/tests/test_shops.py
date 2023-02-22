from random import choice

import pytest
from itertools import cycle

from django.db.models import QuerySet
from mptt.querysets import TreeQuerySet
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED

from shared.mixins import TestFixtures
from shops.models import Shop, Category, Currency
from shops.serializers import ShopSerializer


@pytest.mark.django_db
class TestShopAPIView(TestFixtures):
    def test_create_model(self, faker, obj_shop):
        shops_count = Shop.objects.count()
        self.baker.make(
            'shops.Shop',
            _quantity=20,
            name=self.repeat(faker.name, 20),
            shop_category=cycle(Category.objects.all()),
            shop_currency=cycle(Currency.objects.all()),
            languages=['uz', 'en', 'ru'],
            user=obj_shop.user
        )
        assert Shop.objects.count() == shops_count + 20

    def test_shop_model(self, obj_shop):
        shop = obj_shop

        # Test for __str__ methods of Models
        assert str(shop) == shop.name
        assert str(shop.shop_category) == shop.shop_category.name
        assert str(shop.shop_currency) == shop.shop_currency.name

        # Test for @property methods of Models
        assert isinstance(shop.categories, TreeQuerySet)
        assert isinstance(shop.clients, QuerySet)
        assert isinstance(shop.products, QuerySet)
        assert isinstance(shop.orders, QuerySet)
        assert isinstance(shop.payment_providers, QuerySet)

    def test_get_shops_api(self, client, obj_user, auth_header, obj_shop):
        shop_url = reverse('v1:shops:shop-list')
        response = client.get(shop_url, **auth_header)
        assert response.status_code == HTTP_200_OK
        assert response.data.get('count') == obj_user.shop_set.count()
        shop_config = reverse('v1:shops:shop-shop-config')
        response = client.get(shop_config, **auth_header)
        assert response.status_code == HTTP_200_OK

    def test_create_shops_api(self, client, auth_header, faker, obj_shop, model_shop_categories, model_currencies):
        shop_url = reverse('v1:shops:shop-list')
        data = {
            'name': faker.name(),
            'shop_category': choice(model_shop_categories).pk,
            'shop_currency': choice(model_currencies).pk,
            'languages': {'uz', 'ru'}
        }
        response = client.post(shop_url, data, **auth_header)
        assert response.status_code == HTTP_201_CREATED
        assert response.data['name'] == data['name']
        assert response.data['languages'] == data['languages']

    def test_shop_detail_api(self, client, auth_header, obj_shop):
        url = reverse('v1:shops:shop-detail', kwargs={'pk': obj_shop.pk})
        response = client.get(url, **auth_header)
        assert response.status_code == HTTP_200_OK

        data = {
            'name': 'ShopName'
        }
        response = client.patch(url, data, content_type="application/json", **auth_header)
        assert response.status_code == HTTP_200_OK
        assert response.data.get('name') == data['name']
        assert response.data.get('id') == obj_shop.pk

        response = client.delete(url, **auth_header)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not Shop.objects.filter(pk=obj_shop.pk)  # is really deleted?

    def test_serializer_response(self, obj_shop):
        serializer = ShopSerializer(obj_shop)
        required_fields = (
            'id', 'name', 'shop_category', 'shop_currency', 'languages', 'shop_orders_count', 'shop_clients_count',
            'status', 'shop_status_readable', 'about_us', 'delivery_price', 'delivery_price_per_km', 'lon', 'lat',
            'minimum_delivery_price', 'free_delivery', 'about_us_image', 'expires_at', 'delivery_types', 'has_terminal',
            'created_at', 'starts_at', 'ends_at', 'current_plans', 'delivery_terms', 'shop_category'
        )
        for field in required_fields:
            assert field in serializer.data

    def test_get_all_orders_api(self, client, auth_header, obj_shop):  # TODO to finish
        url = reverse('v1:shops:order-list', (obj_shop.pk,))
        response = client.get(url, **auth_header)
        assert response.status_code == HTTP_200_OK
