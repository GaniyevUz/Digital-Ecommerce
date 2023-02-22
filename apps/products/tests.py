import json
from itertools import cycle
from random import randint, choice

import pytest
from django.contrib.auth.models import Permission
from django.test import Client
from django.urls import reverse_lazy
from faker import Faker
from model_bakery import baker
from rest_framework import status, reverse
from rest_framework_simplejwt.views import TokenObtainPairView

from products.models import Category as PrCategory, Product
from shops.models import Shop, Currency, Category as ShCategory
from users.models import User

faker = Faker()


# Todo: Muhammad Goto apps.shared.mixins.TestFixtures don't edit only see or add something
class FixtureClass:
    def _generate(self, cls):
        return choice(cls.object.all())

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(
            username='admin', password='password'
        )
        for i in Permission.objects.filter(name__endswith='product'):
            user.user_permissions.add(i)
        return user

    @pytest.fixture
    def create_shop(self, user):
        for _ in range(5):
            ShCategory.objects.create(name=faker.first_name())
            Currency.objects.create(name=faker.currency_code())
        baker.make(
            'shops.Shop',
            name=faker.company(),
            shop_category_id=cycle(ShCategory.objects.values_list('id', flat=True)),
            shop_currency_id=cycle(Currency.objects.values_list('id', flat=True)),
            user=user,
            languages=['uz', 'en'],
            _quantity=3
        )
        return Shop.objects.all()

    @pytest.fixture
    def create_category(self, create_shop):
        # shop = Shop.objects.values_list('pk', flat=True)
        baker.make(
            'products.Category',
            name=cycle(faker.sentences(nb=50)),
            description=cycle(faker.texts(nb_texts=5, max_nb_chars=100)),
            shop=cycle(Shop.objects.all()),
            _quantity=5,
        )
        return PrCategory.objects.all()

    @pytest.fixture
    def create_product(self, create_category):
        random_int = [randint(1, 9999) * 100 for i in range(50)]
        baker.make(
            'products.Product',
            name=faker.word(),
            description=faker.sentence(),
            category=cycle(PrCategory.objects.all()),
            image=faker.image_url(),
            price=cycle(random_int),
            in_availability=cycle((True, False)),
            _quantity=20
        )
        return Product.objects.all()


@pytest.mark.django_db
class TestProductManager(FixtureClass):

    def test_get_products_by_created(self, create_product):
        assert ShCategory.objects.count() == 5
        assert PrCategory.objects.count() == 10
        assert Product.objects.count() == 20


@pytest.mark.django_db
class TestProductModelViewSet(FixtureClass):
    client = Client()

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

    def test_list_product(self, client: Client, user, create_product):
        '''
        This test will check 1 page with 10 details in the product class
        '''
        client.force_login(user)
        url = reverse('v1:products:product-list', args=(1,))
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results', 11)) <= 10

    def test_create_product(self, user, create_product, client):
        '''
        This test will check if there are any errors you received
        while creating the product
        '''
        url = reverse_lazy('v1:products:product-list', args=(1,))
        data = {
            'name': 'product1',
            'description': 'description1',
            'category': 1,
            'price': 5000,
            'shop': Shop.objects.first().pk,
            'attributes': [{}]
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        client.force_login(user)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
