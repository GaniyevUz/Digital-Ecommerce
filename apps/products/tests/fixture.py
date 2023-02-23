from itertools import cycle
from random import randint

import pytest
from django.contrib.auth.models import Permission
from model_bakery import baker

from products.models import Category as PrCategory, Product
from shops.models import Shop, Currency, Category as ShCategory
from users.models import User


class FixtureClass:

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(
            username='admin', password='password'
        )
        user.user_permissions.add(*Permission.objects.filter(name__endswith='product'))
        return user

    @pytest.fixture
    def create_shop(self, user, faker):
        for _ in range(5):
            ShCategory.objects.create(name=faker.first_name())
            Currency.objects.create(name=faker.currency_code())
        baker.make(
            'shops.Shop',
            name=faker.company(),
            shop_category=cycle(ShCategory.objects.all()),
            shop_currency=cycle(Currency.objects.all()),
            user=user,
            languages=['uz', 'en'],
            _quantity=3
        )
        return Shop.objects.all()

    @pytest.fixture
    def create_category(self, create_shop, faker):
        baker.make(
            'products.Category',
            name=cycle(faker.sentences(nb=50)),
            description=cycle(faker.texts(nb_texts=5, max_nb_chars=100)),
            shop=cycle(Shop.objects.all()),
            _quantity=5,
        )
        return PrCategory.objects.all()

    @pytest.fixture
    def create_products(self, create_category, faker):
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

    @pytest.fixture
    def create_product(self, create_category, faker):
        category = PrCategory.objects.first()
        return Product.objects.create(
            name=faker.word(),
            description=faker.sentence(),
            category=category,
            price=5600,
            attributes=[{}]
        )
