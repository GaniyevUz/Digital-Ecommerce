import os
from itertools import cycle
from random import choice, choices, randint

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from orders.models import Order
from products.models import Category as ProductCategory, Product
from shared.emojis import all_emojis
from shared.visualize import Loader
from shops.models import Currency, Category, Shop
from users.models import User


class Command(BaseCommand):
    fake = Faker('en')

    @staticmethod
    def repeat(func, count, *args, **kwargs):
        for _ in range(count):
            yield func(*args, **kwargs)

    @staticmethod
    def fake_phone():
        company_codes = ('90', '91', '93', '94', '97', '98', '99', '33')
        numbers = '0123456789'
        return '+998' + choice(company_codes) + ''.join((choice(numbers) for _ in range(7)))

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', type=int, help='Define a fake users number')
        parser.add_argument('-ctg', '--shop_category', type=int, help='Define a fake categories number')
        parser.add_argument('-cur', '--shop_currency', type=int, help='Define a fake currencies number')
        parser.add_argument('-sh', '--shop', type=int, help='Define a fake shops number')
        parser.add_argument('-p', '--product', type=int, help='Define a products number')
        parser.add_argument('-p_c', '--product_category', type=int, help='Define a product categories number')
        parser.add_argument('-o', '--order', type=int, help='Define a orders number')

    def handle(self, *args, **options):
        os.system('make data')
        user = options.get('user')
        shop_category = options.get('shop_category')
        shop_currency = options.get('shop_currency')
        shop = options.get('shop')
        product_category = options.get('product_category')
        product = options.get('product')
        order = options.get('order')

        if user:
            Loader(self.fake_users, user, 'User', user)
        if shop_currency:
            Loader(self.fake_shop_currencies, shop_currency, 'Currency', shop_currency)
        if shop_category:
            Loader(self.fake_shop_categories, shop_category, 'Category', shop_category)
        if shop:
            Loader(self.fake_shops, shop, 'Shop', shop)
        if product_category:
            Loader(self.fake_product_category, product_category, 'ProductCategory', product_category)
        if product:
            Loader(self.fake_product, product, 'Product', product)
        if order:
            Loader(self.fake_orders, order, 'Order', order)

    def fake_users(self, count):
        baker.make(
            'users.User',
            username=self.repeat(self.fake.unique.user_name, count),
            password=make_password('1'),
            first_name=self.repeat(self.fake.unique.first_name, count),
            last_name=self.repeat(self.fake.unique.last_name, count),
            email=self.repeat(self.fake.unique.email, count),
            invitation_token=self.repeat(self.fake.unique.password, count, length=10, special_chars=False),
            _quantity=count
        )

    def fake_shop_categories(self, count):
        baker.make(
            'shops.Category',
            name=self.repeat(self.fake.unique.first_name, count),
            _quantity=count
        )

    def fake_shop_currencies(self, count):
        baker.make(
            'shops.Currency',
            name=self.repeat(self.fake.unique.currency_code, count),
            _quantity=count
        )

    def fake_shops(self, count):
        baker.make(
            'shops.Shop',
            name=self.repeat(self.fake.unique.company, count),
            languages=cycle(choices(['uz', 'en', 'ru'], k=randint(1, 3)) for _ in range(count)),
            delivery_types=cycle(choices(['pickup', 'delivery'], k=randint(1, 2)) for _ in range(count)),
            about_us=self.repeat(self.fake.sentence, count),
            delivery_price=self.repeat(self.fake.random_number, count, digits=5),
            delivery_terms=self.repeat(self.fake.sentence, count),
            user=cycle(User.objects.all()),
            shop_category=cycle(Category.objects.all()),
            shop_currency=cycle(Currency.objects.all()),
            _quantity=count
        )

    def fake_product_category(self, count):
        emoji = all_emojis
        shops = Shop.objects.all()
        baker.make(
            'products.Category',
            name=cycle(self.fake.sentences(nb=100)),
            description=cycle(self.fake.sentences(nb=310050)),
            emoji=cycle(emoji),
            # image='blogs/default.jpg',
            shop=cycle(shops),
            _quantity=count
        )

    def fake_product(self, count):
        categories = ProductCategory.objects.all()

        baker.make(
            'products.Product',
            name=self.repeat(self.fake.unique.first_name, count),
            description=cycle(self.fake.sentences(nb=310050)),
            category=cycle(categories),
            # image='blogs/default.jpg',
            price=self.repeat(self.fake.random_number, count, digits=6),
            in_availability=self.fake.random.choice((True, False)),
            _quantity=count
        )

    def fake_orders(self, count):
        shops = Shop.objects.all()
        # delivery_types = ('pickup', 'delivery')
        baker.make(
            'orders.Order',
            first_name=self.repeat(self.fake.unique.first_name, count),
            last_name=self.repeat(self.fake.unique.last_name, count),
            phone=self.repeat(self.fake_phone, count),
            delivery_type=cycle(choice(['pickup', 'delivery']) for _ in range(count)),
            status=cycle(choice(Order.Status.choices)[0] for _ in range(count)),
            payment_type=cycle(choice(Order.Payment.choices)[0] for _ in range(count)),
            note=self.repeat(self.fake.sentence, count),
            paid=cycle(choice((True, False)) for _ in range(count)),
            shop=cycle(shops),
            # items=self.items(count),
            _quantity=count,
        )

    @staticmethod
    def items(count):
        products = Product.objects.all()
        for _ in range(count):
            yield choices(products, k=randint(1, len(products)))
