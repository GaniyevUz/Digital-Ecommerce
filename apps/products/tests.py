import json
from itertools import cycle
from random import randint

import pytest
from django.contrib.auth.hashers import make_password
from django.test import Client
from django.urls import reverse_lazy
from faker import Faker
from model_bakery import baker
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from products.models import Category as PrCategory, Product
from products.views import ProductModelViewSet
from shops.models import Shop, Currency, Category as ShCategory
from users.models import User

faker = Faker()


@pytest.mark.django_db
class TestProductManager:

    @pytest.fixture
    def create_default_user(self):
        user = User.objects.create(username='default_user', password=make_password('default_pass'))
        return user

    @pytest.fixture
    def create_shop(self, create_default_user):
        for _ in range(5):
            ShCategory.objects.create(name=faker.first_name())
            Currency.objects.create(name=faker.currency_code())
        baker.make(
            'shops.Shop',
            name=faker.company(),
            shop_category_id=cycle(ShCategory.objects.values_list('id', flat=True)),
            shop_currency_id=cycle(Currency.objects.values_list('id', flat=True)),
            user=create_default_user,
            languages=['uz', 'en'],
            _quantity=3
        )
        return Shop.objects.all()

    @pytest.fixture
    def create_category(self, create_shop):
        # parent_category = PrCategory.objects.all()
        shop = Shop.objects.all()
        baker.make(
            'products.Category',
            name=cycle(faker.sentences(nb=50)),
            description=cycle(faker.texts(nb_texts=5, max_nb_chars=100)),
            shop=cycle(shop),
            _quantity=10,
            make_m2m=True
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

    def test_get_products_by_created(self, create_product):
        assert ShCategory.objects.count() == 5
        assert PrCategory.objects.count() == 10
        assert Product.objects.count() == 20


@pytest.mark.django_db
class TestProductModelViewSet:
    client = Client()

    @pytest.fixture
    def create_category(self, admin_user):
        ShCategory.objects.create(name='shop category')
        Currency.objects.create(name='USD')

        shop = Shop.objects.create(name='shop1',
                                   languages=['uz', 'en'],
                                   user=admin_user,
                                   shop_category=ShCategory.objects.first(),
                                   shop_currency=Currency.objects.first())

        PrCategory.objects.create(
            name=faker.sentences(nb=50),
            description=faker.texts(nb_texts=5, max_nb_chars=100),
            shop=shop,
        )

    @pytest.fixture
    def create_product(self, create_category, admin_user):
        Product.objects.create(
            name='product1',
            description='description1',
            category_id=PrCategory.objects.first().id,
            price=5000,
        )
        return Product.objects.first()

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

    @pytest.mark.urls('products.urls')
    def test_list_product(self, rf):
        request = rf.get('url')
        response = ProductModelViewSet.as_view({'get': 'list'})(request).render()
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.urls('products.urls')
    def test_create_product_error(self, rf, create_category, client):
        '''
        This test will check if there are any errors you received
        while creating the product
        '''
        url = reverse_lazy('product-list', args=(1,))
        token = self.auth_header(client, rf)
        data = {
            'name': 'product1',
            'description': 'description1',
            'category_id': PrCategory.objects.first().id,
            # 'image': faker.image(),
            'price': 5000,
        }
        headers = {'HTTP_AUTHORIZATION': 'Bearer ' + token.get('access'), }

        request = rf.post(url, content_type='application/json', data=json.dumps(data))
        response = ProductModelViewSet.as_view({'post': 'create'})(request).render()
        assert response.status_code == status.HTTP_403_FORBIDDEN

        request = rf.post(url, content_type='application/json', data=json.dumps(data), **headers)
        response = ProductModelViewSet.as_view({'post': 'create'})(request).render()
        print()

    @pytest.mark.urls('products.urls')
    def test_update_product(self, rf, create_category, client: Client):
        url = reverse_lazy('product-detail', args=(1, 1))
        # token = self.auth_header(client, rf)
        request = rf.patch(url, content_type='application/json', data=json.dumps({'name': 'new name product'}))
        # product = Product.objects.create(name='product1',
        #                                  description='description1',
        #                                  category=PrCategory.objects.first(),
        #                                  image=faker.image_url(),
        #                                  price=5000
        #                                  )
        response = ProductModelViewSet.as_view({'patch': 'partial_update'})(request).render()
        assert response.status_code == status.HTTP_403_FORBIDDEN
