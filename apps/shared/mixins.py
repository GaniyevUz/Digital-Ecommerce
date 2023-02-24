from random import choice

from django.core.exceptions import ObjectDoesNotExist
from django_hosts import reverse
from django.db.models import QuerySet
from django.urls import reverse
from model_bakery import baker
from pytest import fixture
from rest_framework.status import HTTP_200_OK

from shared.validators import get_subdomain
from shops.models import Currency, Category, Shop
from users.models import User


class BaseShopRequiredMixin:
    def get_queryset(self):
        assert self.queryset is not None, (  # noqa
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset  # noqa

        if shop := self.kwargs.get('shop') is not None:  # noqa
            return queryset.filter(shop=shop)
        # if isinstance(queryset, QuerySet):
        #     queryset = queryset.all()
        return queryset.none()


class ShopRequiredMixin:
    def get_queryset(self):
        if shop_domain := get_subdomain(self.request):  # noqa
            return self.queryset.filter(shop__domain=shop_domain)  # noqa
        return self.queryset.none()  # noqa


class TestFixtures:
    baker = baker

    @fixture
    def obj_user(self) -> User:
        try:
            return User.objects.get(username='default_user')
        except ObjectDoesNotExist:
            return User.objects.create_user(username='default_user', password='default_pass')

    @fixture
    def auth_header(self, obj_user, client):
        token = reverse('v1:users:token_obtain_pair', host='app')
        data = {
            'username': 'default_user',
            'password': 'default_pass'
        }
        response = client.post(token, data)
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
    def obj_shop(self, faker, obj_user, model_shop_categories, model_currencies) -> Shop:
        shop_count = Shop.objects.count()

        shop = Shop.objects.create(
            name=faker.name(), shop_category=choice(model_shop_categories),
            shop_currency=choice(model_currencies), user=obj_user,
            languages=['uz', 'en', 'ru']
        )
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
