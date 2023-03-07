from itertools import cycle
from pprint import pprint

from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from django_hosts import reverse
from model_bakery import baker
from pytest import fixture
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from shared.utils import get_subdomain
from shops.models import Currency, Category, Shop, Country, Domain
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
        return user

    @fixture
    def auth_header(self, obj_user, client):
        token = reverse('api:users:token_obtain_pair', host='api')
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
        assert Shop.objects.count() == shop_count + 1

        return shop

    @fixture
    def domain(self, obj_shop):
        domain, _ = Domain.objects.get_or_create(name='ecommerce', shop=obj_shop)
        return domain

    @fixture
    def obj_category(self, obj_shop, faker):
        category = baker.make('products.Category',
                              name=faker.word(),
                              description=faker.sentence(),
                              shop=obj_shop,
                              _quantity=4
                              )
        return category

    @fixture
    def obj_product(self, obj_category, faker):
        product = baker.make('products.Product',
                             name=faker.word(),
                             description=faker.sentence(),
                             category=cycle(obj_category),
                             price=1000,
                             in_availability=True,
                             _quantity=10
                             )
        return product

    @fixture
    def obj_client(self, obj_shop) -> User:
        client, _ = User.objects.get_or_create(email='client@example.com', password=make_password('client_pass'),
                                               shop=obj_shop)
        return client

    @staticmethod
    def repeat(func, count, *args, **kwargs):
        for _ in range(count):
            yield func(*args, **kwargs)

    @staticmethod
    def t_repeat(func, count, *args, **kwargs):
        for _ in range(count):
            yield {'en': func(*args, **kwargs), 'ru': '', 'uz': ''}


class APIViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)