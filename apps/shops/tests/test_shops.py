from random import choices

import pytest
from django.contrib.auth.hashers import make_password
from django.test import Client
from faker import Faker
from rest_framework.reverse import reverse

from shops.models import Shop, ShopCategory, ShopCurrency
from shops.serializers import ShopSerializer
from users.models import User


@pytest.mark.django_db
class TestShopAPIView:
    @staticmethod
    def get_pk_from_list(values_list):
        return choices(values_list)[0][0]

    fake = Faker()

    @pytest.fixture
    def create_default_user(self):
        user = User.objects.create(username='default_user', password=make_password('default_pass'))
        return user

    @pytest.fixture
    def create_shop_model(self, create_default_user):
        for _ in range(20):
            ShopCategory.objects.create(name=self.fake.first_name())
            ShopCurrency.objects.create(name=self.fake.currency_code())
        return Shop.objects.create(name=self.fake.name(),
                                   shop_category_id=self.get_pk_from_list(ShopCategory.objects.values_list('pk')),
                                   shop_currency_id=self.get_pk_from_list(ShopCurrency.objects.values_list('pk')),
                                   user=create_default_user, languages=['uz', 'en', 'ru'],
                                   )

    def test_create_model(self, create_shop_model):
        for _ in range(20):
            Shop.objects.create(
                name=self.fake.name(),
                shop_category_id=self.get_pk_from_list(ShopCategory.objects.values_list('pk')),
                shop_currency_id=self.get_pk_from_list(ShopCurrency.objects.values_list('pk')),
                languages=['uz', 'en', 'ru'],
                user_id=1
            )
        assert Shop.objects.count() == 21
        assert ShopCategory.objects.count() == 20
        assert ShopCurrency.objects.count() == 20

    @staticmethod
    def auth_header(client):
        token = reverse('v1:users:token_obtain_pair')
        data = {
            'username': 'default_user',
            'password': 'default_pass'
        }
        response = client.post(token, data)
        assert response.status_code == 200
        token = response.data.get('access')
        if token:
            return {'HTTP_AUTHORIZATION': 'Bearer ' + token}

    def test_get_shops_api(self, client: Client, create_shop_model):
        headers = self.auth_header(client)
        shop_url = reverse('v1:shops:shop')
        response = client.get(shop_url, **headers)
        assert response.status_code == 200
        assert response.data.get('count') == 1

    def test_create_shops_api(self, client: Client, create_shop_model):
        headers = self.auth_header(client)
        shop_url = reverse('v1:shops:shop')
        data = {
            'name': self.fake.name(),
            'shop_category': self.get_pk_from_list(ShopCategory.objects.values_list('pk')),
            'shop_currency': self.get_pk_from_list(ShopCurrency.objects.values_list('pk')),
            'languages': {'uz', 'ru'}
        }
        response = client.post(shop_url, data, **headers)
        assert response.status_code == 201
        assert response.data['name'] == data['name']
        assert response.data['languages'] == data['languages']

    def test_shop_detail_api(self, client: Client, create_shop_model):
        url = reverse('v1:shops:detail', kwargs={'pk': create_shop_model.pk})
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

    # def test_serializer_response(self, create_shop_model):
    #     serializer = ShopSerializer(create_shop_model)
    #     _ = serializer.data
    #     assert 'id' in _
    #     assert 'name' in _
    #     assert 'shop_category_id' in _
    #     assert 'shop_currency_id' in _
    #     assert 'languages' in _
    #     assert 'shop_orders_count' in _
    #     assert 'shop_clients_count' in _
    #     assert 'status' in _
    #     assert 'shop_status_readable' in _
    #     assert 'shop_is_seen_orders_count' in _
    #     assert 'about_us' in _
    #     assert 'delivery_price' in _
    #     assert 'delivery_price_per_km' in _
    #     assert 'minimum_delivery_price' in _
    #     assert 'free_delivery' in _
    #     assert 'about_us_image' in _
    #     assert 'expires_at' in _
    #     assert 'delivery_types' in _
    #     assert 'has_terminal' in _
    #     assert 'created_at' in _
    #     assert 'starts_at' in _
    #     assert 'ends_at' in _
    #     assert 'current_plans' in _
    #     assert 'delivery_terms' in _
    #     assert 'shop_category' in _
    #     assert 'lon' in _
    #     assert 'lat' in _
