import json

import pytest
from django.test import Client
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from products.models import Category as PrCategory, Product
from products.tests.fixture import FixtureClass
from shops.models import Shop


@pytest.mark.django_db
class TestProductModelViewSet(FixtureClass):

    @staticmethod
    def auth_header(client, rf):
        data = {
            "username": "admin",
            "password": "password"
        }
        request = rf.post('/api/v1/token/', content_type='application/json',
                          data=json.dumps(data))
        response = TokenObtainPairView.as_view()(request).render()
        data = {
            "access": response.data.get('access'),
            "refresh": response.data.get('refresh'),
        }
        return data

    def test_list_product(self, client: Client, user, create_products):
        '''
        This test will check per page with 10 details in the product class
        '''
        client.force_login(user)
        id = Shop.objects.first().pk
        url = reverse_lazy('v1:products:product-list', args=(id,))
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results', 11)) <= 10

    # @pytest.mark.urls('products.urls')
    def test_create_products(self, user, create_products, client):
        '''
        This test will check if there are any errors you received
        while creating the product
        '''
        category = PrCategory.objects.first()
        shop = category.shop
        url = reverse_lazy('v1:products:product-list', args=(shop.pk,))
        data = {
            'name': 'product1',
            'description': 'description1',
            'category': category.pk,
            'price': 5000,
            'shop': shop.pk,
            'attributes': [{}]
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        client.force_login(user)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_product_detail(self, client, user, create_product):
        product = Product.objects.first()
        shop = product.category.shop
        url = reverse_lazy('v1:products:product-detail', kwargs={'shop': shop.pk, 'pk': product.pk})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # def test_product_update(self, client, user, create_products):
    #     product = user.shop_set.first().categories[0].product_set.first()
    #     shop = product.category.shop
    #     url = reverse_lazy('v1:product-detail', kwargs={'shop': shop.pk, 'pk': product.pk})
    #     data = {
    #         'name': 'new name1',
    #     }
    #     client.force_login(user)
    #     response = client.patch(url, data)
    #     print()

    def test_product_delete(self, client, user, create_products):
        shop = user.shop_set.first()
        product = shop.categories[0].product_set.first()
        url = reverse_lazy('v1:products:product-detail', kwargs={'shop': shop.pk, 'pk': product.pk})
        print()
        client.force_login(user)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(pk=product.pk).exists()
