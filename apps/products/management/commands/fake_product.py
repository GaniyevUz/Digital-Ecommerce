from itertools import cycle
from random import randint, sample

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from products.models import Category, Product
from shops.models import Shop
from users.models import User


class Command(BaseCommand):
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-p', '--product', type=int, help='Define a product count', )
        parser.add_argument('-c', '--category', type=int, help='Define a category count', )

    def handle(self, *args, **options):
        if c := options.get('category', 20):
            parent_category = Category.objects.all()
            shop = Shop.objects.all()
            baker.make(
                'products.Category',
                name=cycle(self.fake.sentences(nb=50)),
                description=cycle(self.fake.texts(nb_texts=5, max_nb_chars=100)),
                shop=cycle(shop),
                _quantity=c,
                make_m2m=True
            )
        if p := options.get('product', 20):
            category = Category.objects.all()
            user = User.objects.all()
            baker.make(
                'products.Product',
                name=cycle(self.fake.sentences(nb=50)),
                description=cycle(self.fake.texts(nb_texts=5, max_nb_chars=100)),
                category=cycle(category),
                in_availability=cycle((True, False)),
                price=cycle(sample(range(10, 90), 10)),
                _quantity=p,
                make_m2m=True
            )
