from itertools import cycle

import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django_hosts import reverse, reverse_host
from django.test.utils import override_settings
from model_bakery import baker
from rest_framework import status
from django.test.client import Client as TestClient
from rest_framework.status import HTTP_200_OK
from ecommerce.models import Client
from products.models import Category, Product
from products.tests.fixture import FixtureClass
from shops.models import Domain
from users.models import User


# @override_settings(DEFAULT_HOST='other')
@pytest.mark.django_db
class TestEcommerce:
    @pytest.fixture
    def user(self):
        user, _ = User.objects.get_or_create(email='admin@mail.com', password='password')
        return user

    @pytest.fixture
    def create_shop(self, user, faker):
        shop = baker.make('shops.Shop',
                          name=faker.company(),
                          user=user,
                          languages=['uz', 'en'],
                          make_m2m=True,
                          )
        return shop

    @pytest.fixture
    def domain(self, create_shop):
        domain, _ = Domain.objects.get_or_create(name='ecommerce', shop=create_shop)
        return domain

    @pytest.fixture
    def create_category(self, create_shop, faker):
        category = baker.make('products.Category',
                              name=faker.word(),
                              description=faker.sentence(),
                              shop=create_shop,
                              make_m2m=True,
                              _quantity=4
                              )
        return category

    @pytest.fixture
    def create_product(self, create_category, faker):
        product = baker.make('products.Product',
                             name=faker.word(),
                             description=faker.sentence(),
                             category=cycle(create_category),
                             price=1000,
                             in_availability=True,
                             make_m2m=True,
                             _quantity=10
                             )
        return product

    @pytest.fixture
    def obj_client(self, create_shop) -> User:
        client, _ = Client.objects.get_or_create(email='client@example.com', password=make_password('client_pass'),
                                                 shop=create_shop)
        return client

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

    def test_client_sign_up(self, client: TestClient, domain):
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
        for key in response:
            assert response[key] == data[key]

    def test_client_sign_in(self, client: TestClient, obj_client, domain):
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

    # def test_client_sign_out(self, client: TestClient, obj_client, domain):
    #     server_name = reverse_host('other', (domain.name,))
    #     url = reverse('api:ecommerce:sign-out', host='other', host_args=(domain.name,))
    #     response = client.get(url, SERVER_NAME=server_name)
    #     assert response.status_code == status.HTTP_200_OK

    def test_client_profile(self, client: TestClient, obj_client, domain, auth_header):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:ecommerce:profile', host='other', host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name, **auth_header)
        # assert response.status_code != status.HTTP_401_UNAUTHORIZED
        assert response.status_code == status.HTTP_200_OK
        user = response.json()['user']
        for key in user:
            assert user[key] == getattr(obj_client, key)

    def test_client_profile_destroy(self, client: TestClient, obj_client, domain, auth_header):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:ecommerce:profile', host='other', host_args=(domain.name,))
        response = client.delete(url, SERVER_NAME=server_name, **auth_header)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = client.delete(url, SERVER_NAME=server_name, **auth_header)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_client_profile_update(self, client: TestClient, obj_client, domain, auth_header):
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

    def test_category_list(self, client: TestClient, domain):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:products:category-list', host='other', host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['count'] == domain.shop.category_set.count()

    def test_category_retrieve(self, client: TestClient, domain, create_category):
        category = domain.shop.category_set.first()
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:products:category', args=(category.id,), host='other',
                      host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for key in data:
            assert getattr(category, key) == data[key]

    def test_ecommerce_product_list(self, client, domain):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:products:product-list', host='other', host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name)
        assert response.status_code == status.HTTP_200_OK

    def test_ecommerce_product_detail(self, client, domain, create_product):
        server_name = reverse_host('other', (domain.name,))
        url = reverse('api:products:product-detail', args=(create_product[0].id,), host='other',
                      host_args=(domain.name,))
        response = client.get(url, SERVER_NAME=server_name)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for key in data:
            assert getattr(create_product[0], key) == data[key]
