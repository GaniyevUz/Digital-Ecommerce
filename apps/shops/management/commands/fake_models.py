import os
from itertools import cycle
from random import choice, randint

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from shared.visualize import Loader
from shops.models import Currency, Category, Shop
from users.models import User
from products.models import Category as pr_category, Product


class Command(BaseCommand):
    fake = Faker()

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

    def fake_product_category(self, count):
        emoji = ('🎽', '👔', '👚', '👕', '🧣', '🧕🏻',
                 '💻', '🖥', '📱', '📟', '☎', '️📠', '📱', '📺', '✔', '📌', '🏷', '📦', '🚘', '🧊', '❄', '💨', '🌬',
                 '⌚', '🗄',
                 '🆕', '🔴',
                 '🟠', '🟡', '🟢', '🔵', '🟣', '🔘', '🎁', '💧', '🔖', '📕', '📖', '📓', '📔', '📘', '📚', '📙', '📗',
                 '📒',
                 '🔖', '📑',
                 '💄', '💋', '👄', '👅', '🔮', '⚱', '🧬', '🕳', '🧼', '🖌', '🖍', '👛', '👝', '👜', '🎒', '🛄', '🛍',
                 '🍫', '🍟', '🥓', '🍍', '🥙', '🍯', '🥐', '🍬', '🥟', '🥦', '🍙', '🍣', '🥩', '🥗', '🍩', '🍊', '🍨',
                 '🥔',
                 '🍛', '🍌', '🌯',
                 '🍚', '🍜', '🥤', '🍲', '🧆',
                 '🍮', '🌽', '🍧', '🍓', '🥜', '🍢', '🍋', '🥚', '🍖', '🍡', '🍈', '🌶', '🍞', '🥬', '🦑', '🥡', '🍰',
                 '🌭',
                 '🍘', '🍭', '🦀', '🍦', '🥞',
                 '🌮', '🦐', '🍏', '🍿', '🍠', '🍱', '🍆', '🥥', '🌰', '🥑', '🎂', '🥯', '🍝', '🥫', '🧀', '🍇', '🍉',
                 '🥘',
                 '🍕', '🥝', '🍐', '🥨', '🍒',
                 '🍤', '🍪', '🥖', '🥣', '🍅', '🍎', '🍳', '🍲', '🥠', '🦞', '🍗', '🍥', '🥕', '🍑', '🧂', '🥭', '🥧',
                 '🥪',
                 '😋', '🥒', '🧁', '🍄', '🍔', '🥮',
                 '📺', '📻', '⏰', '🕰', '📡', '🗑', '🔦', '🔧', '🔩', '⚙', '️⛏', '🛠', '⚒', '🔨', '🔪', '🗡', '⚔', '️⚰',
                 '️🧱',
                 '🔭', '🧯',
                 '🚽', '🚰', '🚿', '🔬', '🛁', '🛀', '🧺', '🛎', '🧻', '🛌', '🛏', '🎁', '🛒', '🧳',
                 '🚪', '🧳', '🛌', '🛏',
                 '🤾', '🚴', '🤸', '️⛳', '🏌', '️️🏌', '️🏃', '️🤸', '🤾', '🏄', '‍🧘', '‍🏑', '💪', '🥅', '🤾', '️🏇',
                 '🤽',
                 '️🎾', '🛷',
                 '🥍', '⛹', '️⚾', '🤼', '🏀', '🎱', '🏸', '🚵', '️🏆', '🏉', '🏐', '🚙', '🏟', '🥌',
                 '🏓', '🤺', '🏅', '🎿', '🏊', '️🥉', '🏃', '‍️🏋', '️‍️🏒', '🤼', '️🤼', '‍️🥈', '🏊', '‍️🚣', '‍️🤽',
                 '‍️🏈',
                 '🚴‍', '️🎯', '🏏', '⛷',
                 '🎣', '🏄', '‍️🤸', '🥋', '🏋', '️‍️🥎', '🎳', '🎽', '🥇', '🚣', '‍️🏂', '⛹️‍', '️🥊', '⛸',
                 '🧸', '🐻', '🦊', '🐹', '🐷', '🦄', '🐇', '🐿', '⛄', '️🚌', '🚎', '🚚', '✈', '️🚀', '🚁', '🛳',
                 '💿', '💾', '✉', '📩', '📨', '📧', '💌', '📥', '📤', '📦', '🏷', '📪', '📫', '📬', '📭', '📮', '📯',
                 '📜',
                 '📃', '📄', '📑',
                 '📊', '📈', '📉', '🗒', '🗓', '📆', '📅', '📇', '🗃', '🔏', '🔐', '🔒', '🔓',
                 '🗳', '🗄', '📋', '📁', '📂', '🗂', '🗞', '📰', '📓', '📔', '📒', '📕', '📗', '📘', '📙', '📚', '📖',
                 '🔖',
                 '🔗', '📎', '🖇', '📐',
                 '📏', '📌', '📍', '✂', '🖊', '🖋', '✒', '🖌', '🖍', '📝', '✏', '️🔍', '🔎',
                 '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🦝', '🐻', '🐼', '🦘', '🦡', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽',
                 '🐸',
                 '🐵', '🙈', '🙉', '🙊',
                 '🐒', '🐔', '🐧',
                 '🦢', '🦅', '🦉', '🦚', '🦜', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐚', '🐞', '🐜',
                 '🦗',
                 '🕷', '🕸', '🦂', '🦟', '🦠', '🐢', '🐍',

                 '🦐', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆', '🦓', '🦍', '🐘', '🦏', '🦛',
                 '🐪', '🐫',
                 '🦙', '🐤', '🐣', '🐥', '🦆', '🐦', '🦎', '🐀', '🐿', '🦔', '🐾', '🦕', '🐙', '🦑', '🦖', '⚡' '🦒',
                 '🐃', '🐂',
                 '🐄', '🐎', '🐖', '🐏', '🐑', '🐐', '🦌', '🐕', '🐩', '🐈', '🐓', '🦃', '🕊', '🐇', '🐁',)
        shops = Shop.objects.all()
        baker.make(
            'products.Category',
            name=cycle(self.fake.sentences(nb=100)),
            description=cycle(self.fake.sentences(nb=310050)),
            emoji=cycle(emoji),
            # image='blogs/default.jpg',
            shop=cycle(shops),
            _quantity=count,
            make_m2m=True
        )

    def fake_product(self, count):
        categories = pr_category.objects.all()

        baker.make(
            'products.Product',
            name=cycle((self.fake.unique.first_name() for _ in range(count))),
            description=cycle(self.fake.sentences(nb=310050)),
            category=cycle(categories),
            # image='blogs/default.jpg',
            price=cycle((self.fake.random_number() for _ in range(count))),
            in_availability=self.fake.random.choice((True, False)),
            _quantity=count
        )

    def fake_orders(self, count):
        shops = Shop.objects.all()
        products = baker.prepare('products.Product', count)
        delivery_types = ('pickup', 'delivery')
        baker.make(
            'orders.Order',
            first_name=cycle((self.fake.unique.first_name() for _ in range(count))),
            last_name=cycle((self.fake.unique.last_name() for _ in range(count))),
            phone=cycle((self.fake_phone() for _ in range(count))),
            delivery_type='pickup',
            shop=cycle(shops),
            # items=products,
            _quantity=count,
            make_m2m=True
        )

    def fake_phone(self):
        company_codes = ('90', '91', '93', '94', '97', '98', '99', '33')
        numbers = '0123456789'
        return '+998' + choice(company_codes) + ''.join((choice(numbers) for _ in range(7)))
