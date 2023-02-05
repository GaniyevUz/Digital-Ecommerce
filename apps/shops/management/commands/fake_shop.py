import os
import random
import sys
from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from shops.models import Shop, Currency, Category
from users.models import User


class Command(BaseCommand):
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-q', '--shop', type=int, help='Define a blog number prefix', )
        parser.add_argument('-c', '--category', type=int, help='Define a category number prefix', )

    def handle(self, *args, **options):
        q = options.get('shop', 20)
        os.system('make data')
        category = Category.objects.all()
        currency = Currency.objects.all()
        user = User.objects.all()
        baker.make(
            'shops.Shop',
            name=cycle(self.fake.sentences(nb=50)),
            shop_category=cycle(category),
            shop_currency=cycle(currency),
            user=cycle(user),
            languages=['uz', 'en', 'ru'],
            _quantity=q,
            make_m2m=True
        )
