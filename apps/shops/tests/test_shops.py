from random import choice

import pytest
from django.contrib.auth.hashers import make_password
from django.test import Client
from faker import Faker
from rest_framework.reverse import reverse

from shops.models import Shop, Category, Currency
from shops.serializers import ShopSerializer
from users.models import User


@pytest.mark.django_db
class TestShopAPIView:
    fake = Faker()

    @pytest.fixture
    def create_default_user(self):
        user = User.objects.create(
            username='default_user',
            password=make_password('default_pass')
        )
        return user

    @pytest.fixture
    def create_shop_model(self, create_default_user):
        for _ in range(20):
            Category.objects.create(name=self.fake.first_name())
            Currency.objects.create(name=self.fake.currency_code())

        shop = Shop.objects.create(
            name=self.fake.name(),
            shop_category_id=choice(Category.objects.values_list('pk', flat=True)),
            shop_currency_id=choice(Currency.objects.values_list('pk', flat=True)),
            user=create_default_user, languages=['uz', 'en', 'ru'],
        )
        return shop

    def test_create_model(self, create_shop_model):
        for _ in range(20):
            Shop.objects.create(
                name=self.fake.name(),
                shop_category_id=choice(Category.objects.values_list('pk', flat=True)),
                shop_currency_id=choice(Currency.objects.values_list('pk', flat=True)),
                languages=['uz', 'en', 'ru'],
                user_id=1
            )
        assert Shop.objects.count() == 21
        assert Category.objects.count() == 20
        assert Currency.objects.count() == 20

    @staticmethod
    def auth_header(client):
        token = reverse('v1:users:token_obtain_pair')
        data = {
            'username': 'default_user',
            'password': 'default_pass'
        }
        response = client.post(token, data)
        assert response.status_code == 200
        if token := response.data.get('access'):
            return {'HTTP_AUTHORIZATION': 'Bearer ' + token}

    def test_shop_model(self, create_shop_model):
        shop = create_shop_model
        assert str(shop) == shop.name
        assert shop.categories.count() == shop.category_set.count()
        assert shop.clients.count() == shop.client_set.count()
        assert shop.products.count() == shop.product_set.count()
        assert shop.orders.count() == shop.order_set.count()

    def test_get_shops_api(self, client: Client, create_shop_model):
        headers = self.auth_header(client)
        shop_url = reverse('v1:shops:shop-list')
        response = client.get(shop_url, **headers)
        assert response.status_code == 200
        assert response.data.get('count') == 1
        shop_config = reverse('v1:shops:shop-shop-config')
        response = client.get(shop_config, **headers)
        assert response.status_code == 200

    def test_create_shops_api(self, client: Client, create_shop_model):
        headers = self.auth_header(client)
        shop_url = reverse('v1:shops:shop-list')
        data = {
            'name': self.fake.name(),
            'shop_category': choice(Category.objects.values_list('pk', flat=True)),
            'shop_currency': choice(Currency.objects.values_list('pk', flat=True)),
            'languages': {'uz', 'ru'}
        }
        response = client.post(shop_url, data, **headers)
        assert response.status_code == 201
        assert response.data['name'] == data['name']
        assert response.data['languages'] == data['languages']

    def test_shop_detail_api(self, client: Client, create_shop_model):
        url = reverse('v1:shops:shop-detail', kwargs={'pk': create_shop_model.pk})
        headers = self.auth_header(client)
        response = client.get(url, **headers)
        assert response.status_code == 200

        data = {
            'name': 'ShopName'
        }
        response = client.patch(url, data, content_type="application/json", **headers)
        assert response.status_code == 200
        assert response.data.get('name') == data['name']
        assert response.data.get('id') == create_shop_model.pk

        response = client.delete(url, **headers)
        assert response.status_code == 204
        assert Shop.objects.count() == 0

    def test_serializer_response(self, create_shop_model):
        serializer = ShopSerializer(create_shop_model)
        _ = serializer.data
        assert 'id' in _  # TODO to optimize
        assert 'name' in _
        assert 'shop_category' in _
        assert 'shop_currency' in _
        assert 'languages' in _
        assert 'shop_orders_count' in _
        assert 'shop_clients_count' in _
        assert 'status' in _
        assert 'shop_status_readable' in _
        assert 'about_us' in _
        assert 'delivery_price' in _
        assert 'delivery_price_per_km' in _
        assert 'minimum_delivery_price' in _
        assert 'free_delivery' in _
        assert 'about_us_image' in _
        assert 'expires_at' in _
        assert 'delivery_types' in _
        assert 'has_terminal' in _
        assert 'created_at' in _
        assert 'starts_at' in _
        assert 'ends_at' in _
        assert 'current_plans' in _
        assert 'delivery_terms' in _
        assert 'shop_category' in _
        assert 'lon' in _
        assert 'lat' in _

    def test_get_all_orders_api(self, client, create_shop_model):  # TODO to finish
        headers = self.auth_header(client)
        url = reverse('v1:shops:order-list', (create_shop_model.pk,))
        response = client.get(url, **headers)
        assert response.status_code == 200
