import pytest
from django_hosts import reverse, reverse_host
from django.test.utils import override_settings
from rest_framework import status
from django.test.client import Client as TestClient
from rest_framework.status import HTTP_200_OK
from ecommerce.models import Client
from products.tests.fixture import FixtureClass
from shops.models import Domain
from users.models import User


# @override_settings(DEFAULT_HOST='other')
@pytest.mark.django_db
class TestEcommerce(FixtureClass):

    @pytest.fixture
    def domain(self, create_shop):
        shop = create_shop.first()
        domain, _ = Domain.objects.get_or_create(name='ecommerce', shop=shop)
        return domain

    @pytest.fixture
    def obj_client(self) -> User:
        client, _ = Client.objects.get_or_create(email='client@mail.com', password='client_pass')
        return client

    @pytest.fixture
    def auth_header(self, obj_client, client):
        token = reverse('api:users:token_obtain_pair', host='api')
        data = {
            'email': obj_client.email,
            'password': 'client_pass'
        }
        response = client.post(token, data)
        assert response.status_code == HTTP_200_OK
        if token := response.data.get('access'):
            return {'HTTP_AUTHORIZATION': 'Bearer ' + token}

    def test_ecommerce_product_list(self, client, domain):
        url = reverse('api:products:product-list', host='other', host_args=(domain.name,))
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_client_sign_up(self, client: TestClient, rf, admin_user, domain):
        url = reverse('api:ecommerce:sign-up', host='other', host_args=(domain.name,))
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
