import pytest
from django.test import Client
from django_hosts import reverse
from rest_framework import status

from products.models import Category as PrCategory, Product
from products.tests.fixture import FixtureClass
from shops.models import Shop


@pytest.mark.django_db
class TestProductAPIViewSet(FixtureClass):

    def test_list_product(self, client: Client, user):
        '''
        This test will check per page with 10 details in the product class
        '''
        client.force_login(user)
        shop = Shop.objects.first()
        url = reverse('api:shops:product-list', kwargs={'shop': shop.pk}, host='api')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results', 11)) <= 10

    # @pytest.mark.urls('products.urls')
    def test_create_products(self, user, client):
        '''
        This test will check if there are any errors you received
        while creating the product
        '''
        category = PrCategory.objects.first()
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
        assert response.status_code == status.HTTP_403_FORBIDDEN

        client.force_login(user)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_product_detail(self, client):
        product = Product.objects.first()
        shop = product.category.shop
        url = reverse('api:shops:product-detail', args=(shop.pk, product.pk), host='api')

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_product_update(self, client, user):
        product = user.shop_set.first().categories[0].product_set.first()
        shop = product.category.shop
        url = reverse('api:shops:product-detail', args=(shop.pk, product.pk), host='api')
        data = {
            'name': 'new name1',
        }
        client.force_login(user)
        response = client.patch(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == data.get('name')

    def test_product_delete(self, client, user):
        shop = user.shop_set.first()
        product = shop.categories[0].product_set.first()
        url = reverse('api:shops:product-detail', args=(shop.pk, product.pk), host='api')
        client.force_login(user)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(pk=product.pk).exists()
