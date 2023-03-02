import pytest
from django.test.client import Client
from django_hosts import reverse, reverse_host
from rest_framework import status
from rest_framework.status import HTTP_200_OK

from products.serializers import ProductModelSerializer, CategoryModelSerializer
from shared.mixins import TestFixtures


# @override_settings(DEFAULT_HOST='other')
@pytest.mark.django_db
class TestEcommerce(TestFixtures):

    @pytest.fixture
    def auth_header(self, obj_client, client, domain):
        url = reverse('api:ecommerce:sign-in', host='other', host_args=(domain.name,))
        data = {
            'email': obj_client.email,
            'password': 'client_pass'
        }
        server_name = reverse_host('other', (domain.name,))
        response = client.post(url, data, SERVER_NAME=server_name)
        assert response.status_code == HTTP_200_OK
        if token := response.data.get('access'):
            return {'HTTP_AUTHORIZATION': 'Bearer ' + token}

    def test_client_sign_up(self, client: Client, domain):
        data = {
            'password': '@DK@Gdu236gc2bf23',
            'confirm_password': '@DK@Gdu236gc2bf23',
            'email': 'user@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+998901234567',
            'account_type': 'email'
        }
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:ecommerce:sign-up', host='other', host_args=(domain.name,))
        response = client.post(url, data, SERVER_NAME=server_name)
        assert response.status_code == status.HTTP_201_CREATED
        response = response.json()['user']
        del response['id']
        for key in response:
            assert response[key] == data[key]

    def test_client_sign_in(self, client: Client, obj_client, domain):
        data = {
            'password': 'client_pass',
            'email': obj_client.email
        }
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:ecommerce:sign-in', host='other', host_args=(domain.name,))
        response = client.post(url, data, SERVER_NAME=server_name)

        assert response.status_code == status.HTTP_200_OK
        user = response.json()['user']
        for key in user:
            assert user[key] == getattr(obj_client, key)
        assert response.json()['access'] is not None
        assert response.json()['refresh'] is not None

    # def test_client_sign_out(self, client: Client, obj_client, domain):
    #     server_name = reverse_host('other', (domain.name,))
    #     url = reverse('api:ecommerce:sign-out', host='other', host_args=(domain.name,))
    #     response = client.get(url, SERVER_NAME=server_name)
    #     assert response.status_code == status.HTTP_200_OK

    def test_client_profile(self, client: Client, obj_client, domain, auth_header):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:ecommerce:profile', host='other', host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name, **auth_header)
        assert response.status_code == status.HTTP_200_OK
        user = response.json()['user']
        for key in user:
            assert user[key] == getattr(obj_client, key)

    def test_client_profile_update(self, client: Client, obj_client, domain, auth_header):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:ecommerce:profile', host='other', host_args=(domain.name,))
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+998901234567',
        }
        response = client.put(url, data, SERVER_NAME=server_name, **auth_header)
        assert response.status_code == status.HTTP_200_OK
        user = response.json()['user']
        for key in user:
            assert user[key] == data[key]

    def test_client_profile_destroy(self, client: Client, obj_client, domain, auth_header):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:ecommerce:profile', host='other', host_args=(domain.name,))
        response = client.delete(url, SERVER_NAME=server_name, **auth_header)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = client.delete(url, SERVER_NAME=server_name, **auth_header)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_category_list(self, client: Client, domain):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:products:category-list', host='other', host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['count'] == domain.shop.category_set.count()

    def test_category_retrieve(self, client: Client, domain, obj_category):
        category = domain.shop.category_set.first()
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:products:category', args=(category.id,), host='other',
                      host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        category = CategoryModelSerializer(category).data
        for key in data:
            assert category[key] == data[key]

    def test_ecommerce_product_list(self, client, domain):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:products:product-list', host='other', host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name)
        assert response.status_code == status.HTTP_200_OK

    def test_ecommerce_product_detail(self, client, domain, obj_product):
        product = obj_product[0]
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:products:product-detail', args=(product.id,), host='other',
                      host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name)
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        product = ProductModelSerializer(product).data
        for key in data:
            assert product[key] == data[key]
