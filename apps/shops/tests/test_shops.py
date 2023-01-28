from pprint import pprint
from random import randint

import pytest
from django.contrib.auth.hashers import make_password
from django.test import Client
from faker import Faker
from model_bakery import baker
from model_bakery.baker import Baker
from rest_framework.reverse import reverse

from shops.models import Shop, ShopCategory, ShopCurrency
from users.models import User


@pytest.mark.django_db
class TestShopAPIView:
    fake = Faker()
    Faker.seed(0)

    @pytest.fixture
    def create_default_user(self):
        user = User.objects.create(username='default_user', password=make_password('default_pass'))
        return user

    @pytest.fixture
    def create_shop_models(self, create_default_user):
        baker.make(ShopCategory, _quantity=20, _bulk_create=True, name=self.fake.first_name())
        baker.make(ShopCurrency, _quantity=20, _bulk_create=True, name=self.fake.currency_code())
        Shop.objects.create(name=self.fake.name(), shop_category_id=randint(1, 10),
                            shop_currency_id=randint(1, 10), user_id=1, languages=['uz', 'en', 'ru'],
                            )

    def test_create_model(self, create_shop_models):
        for i in range(20):
            Shop.objects.create(
                name=self.fake.name(),
                shop_category_id=randint(1, 20),
                shop_currency_id=randint(1, 20),
                languages=['uz', 'en', 'ru'],
                user_id=1
            )
        assert Shop.objects.count() == 21
        assert ShopCategory.objects.count() == 20
        assert ShopCurrency.objects.count() == 20

    @staticmethod
    def get_access_token(client):
        token = reverse('v1:users:token_obtain_pair')
        data = {
            'username': 'default_user',
            'password': 'default_pass'
        }
        return client.post(token, data)

    def test_get_shops_api(self, client: Client, create_default_user):
        access_response = self.get_access_token(client)
        assert access_response.status_code == 200
        access_token = access_response.data.get('access')
        shop_url = reverse('v1:shops:shop')
        response = client.get(shop_url, HTTP_AUTHORIZATION='Bearer ' + access_token)
        assert response.status_code == 200

    def test_create_shops_api(self, client: Client, create_shop_models):
        access_response = self.get_access_token(client)
        assert access_response.status_code == 200
        access_token = access_response.data.get('access')
        shop_url = reverse('v1:shops:shop')
        print(ShopCategory.objects.values_list('pk', 'name'), ShopCategory.objects.count())
        print(ShopCurrency.objects.values_list('pk', 'name'), ShopCurrency.objects.count())
        data = {
            'name': self.fake.name(),
            'shop_category': randint(1, 10),
            'shop_currency': randint(1, 10),
            'languages': ['uz', 'ru']
        }
        response = client.post(shop_url, data, HTTP_AUTHORIZATION='Bearer ' + access_token)
        pprint(response)
        assert response.status_code == 201
        assert response.data['name'] == data['name']
        assert response.data['languages'] == data['languages']
