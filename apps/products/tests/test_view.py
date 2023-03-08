import pytest
from django.test import Client
from django_hosts import reverse
from rest_framework import status

from products.models import Category as PrCategory, Product
from products.tests.fixture import FixtureClass
from shared.django import TestFixtures
from shops.models import Shop


@pytest.mark.django_db
class TestProductAPIViewSet(TestFixtures):

    def test_list_product(self, client: Client, obj_user, obj_shop):
        url = reverse('api:shops:product-list', kwargs={'shop': obj_shop.pk}, host='api')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results', 11)) <= 10

    # @pytest.mark.urls('products.urls')
    def test_create_products(self, client, obj_category, auth_header):
        category = obj_category[0]
        shop = category.shop
        url = reverse('api:shops:product-list', kwargs={'shop': shop.pk}, host='api')

        data = {
            'name': 'product1',
            'description': 'description1',
            'category': category.pk,
            'price': 5000,
            'attributes': [{}]
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = client.post(url, data, **auth_header)
        assert response.status_code == status.HTTP_201_CREATED

    def test_product_detail(self, client, obj_product):
        shop = obj_product[0].category.shop
        url = reverse('api:shops:product-detail', args=(shop.pk, obj_product[0].pk), host='api')

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_product_update(self, client, obj_product, auth_header):
        product = obj_product[0]
        shop = product.category.shop
        url = reverse('api:shops:product-detail', args=(shop.pk, product.pk), host='api')
        data = {
            'name': 'new name1',
        }
        response = client.patch(url, data, 'application/json', **auth_header)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == data.get('name')

    def test_product_delete(self, client, obj_product, auth_header):
        product = obj_product[0]
        url = reverse('api:shops:product-detail', args=(product.category.shop.pk, product.pk), host='api')
        response = client.delete(url, **auth_header)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(pk=product.pk).exists()
