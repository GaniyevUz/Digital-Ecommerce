from pprint import pprint
from random import choice

from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django_hosts import reverse
from model_bakery import baker
from pytest import fixture
from rest_framework.status import HTTP_200_OK

from shared.validators import get_subdomain
from shops.models import Currency, Category, Shop, Country
from users.models import User


class BaseShopMixin:
    @property
    def get_shop(self):
        if shop_id := self.kwargs.get('shop'):  # noqa
            return get_object_or_404(Shop, pk=shop_id)
        if domain := get_subdomain(self.request):  # noqa
            return get_object_or_404(Shop, domain=domain)
        return None

    def get_queryset(self):
        return self.queryset.filter(shop=self.get_shop)  # noqa


class TestFixtures:
    baker = baker

    @fixture
    def obj_user(self) -> User:
        user, _ = User.objects.get_or_create(email='default_user@example.com', password=make_password('default_pass'))
        print(user)
        return user

    @fixture
    def auth_header(self, obj_user, client):
        token = reverse('api:users:token_obtain_pair', host='api')
        print(obj_user)
        data = {
            'email': obj_user.email,
            'password': 'default_pass'
        }
        response = client.post(token, data)
        pprint(response.json())
        assert response.status_code == HTTP_200_OK
        if token := response.data.get('access'):
            return {'HTTP_AUTHORIZATION': 'Bearer ' + token}

    @fixture
    def model_shop_categories(self, faker) -> list:
        cat_count = Category.objects.count()

        self.baker.make(
            'shops.Category',
            _quantity=20,
            name=self.repeat(faker.first_name, 20)
        )

        categories = Category.objects.all()
        assert categories.count() == cat_count + 20

        return categories

    @fixture
    def model_currencies(self, faker) -> list:
        cur_count = Currency.objects.count()

        self.baker.make(
            'shops.Currency',
            _quantity=20,
            name=self.repeat(faker.currency_code, 20)
        )

        currencies = Currency.objects.all()
        assert currencies.count() == cur_count + 20

        return currencies

    @fixture
    def model_countries(self, faker) -> list:
        country_count = Country.objects.count()

        self.baker.make(
            'shops.Country',
            _quantity=20,
            name=self.repeat(faker.unique.country, 20)
        )

        countries = Country.objects.all()
        assert countries.count() == country_count + 20

        return countries

    @fixture
    def obj_shop(self, faker, obj_user) -> Shop:
        shop_count = Shop.objects.count()
        shop = self.baker.make('shops.Shop',
                               name=faker.name(), user=obj_user,
                               languages=['uz', 'en', 'ru']
                               )
        self.baker.make('shops.TelegramBot', token='token', username='username', shop=shop)
        self.baker.make('shops.Domain', name='domain', shop=shop)
        assert Shop.objects.count() == shop_count + 1

        return shop

    @staticmethod
    def repeat(func, count, *args, **kwargs):
        for _ in range(count):
            yield func(*args, **kwargs)

    @staticmethod
    def t_repeat(func, count, *args, **kwargs):
        for _ in range(count):
            yield {'en': func(*args, **kwargs), 'ru': '', 'uz': ''}
