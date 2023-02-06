import os
from itertools import cycle

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from shared.visualize import Loader
from shops.models import Currency, Category
from users.models import User


class Command(BaseCommand):
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', type=int, help='Define a fake users number')
        parser.add_argument('-ctg', '--shop_category', type=int, help='Define a fake categories number')
        parser.add_argument('-cur', '--shop_currency', type=int, help='Define a fake currencies number')
        parser.add_argument('-sh', '--shop', type=int, help='Define a fake shops number')
        parser.add_argument('-c', '--category', type=int, help='Define a category number prefix')

    def handle(self, *args, **options):
        os.system('make data')
        user = options.get('user')
        shop_category = options.get('shop_category')
        shop_currency = options.get('shop_currency')
        shop = options.get('shop')

        if user:
            Loader(self.fake_users, user, 'User', user)
        if shop_currency:
            Loader(self.fake_shop_currencies, shop_currency, 'Currency', shop_currency)
        if shop_category:
            Loader(self.fake_shop_categories, shop_category, 'Category', shop_category)
        if shop:
            Loader(self.fake_shops, shop, 'Shop', shop)

        # q = options.get('shop', 20)
        # os.system('make data')
        # category = Category.objects.all()
        # currency = Currency.objects.all()
        # user = User.objects.all()
        # baker.make(
        #     'shops.Shop',
        #     name=cycle(self.fake.sentences(nb=50)),
        #     shop_category=cycle(category),
        #     shop_currency=cycle(currency),
        #     user=cycle(user),
        #     languages=['uz', 'en', 'ru'],
        #     _quantity=q,
        #     make_m2m=True
        # )

    def fake_users(self, count):
        baker.make(
            'users.User',
            username=cycle((self.fake.unique.user_name() for _ in range(count))),
            password=make_password('1'),
            _quantity=count
        )

    def fake_shop_categories(self, count):
        baker.make(
            'shops.Category',
            name=cycle((self.fake.unique.first_name() for _ in range(count))),
            _quantity=count
        )

    def fake_shop_currencies(self, count):
        baker.make(
            'shops.Currency',
            name=cycle((self.fake.unique.currency_code() for _ in range(count))),
            _quantity=count
        )

    def fake_shops(self, count):
        baker.make(
            'shops.Shop',
            name=cycle((self.fake.unique.company() for _ in range(count))),
            languages=['uz', 'en', 'ru'],
            user=cycle(User.objects.all()),
            shop_category=cycle(Category.objects.all()),
            shop_currency=cycle(Currency.objects.all()),
            _quantity=count,
            make_m2m=True
        )