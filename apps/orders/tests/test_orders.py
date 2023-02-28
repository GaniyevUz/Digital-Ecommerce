import pytest
from django.contrib.auth.hashers import make_password

from orders.models import Order
from products.models import Product, Category as ProductCategory
from shops.models import Shop, Currency, Category
from users.models import User


@pytest.mark.django_db
class TestOrderAPI:
    @pytest.fixture
    def create_user(self):
        user = User.objects.create(
            first_name='Elizabeth',
            last_name='Liz',
            email='elizabeth@liz.io',
            password=make_password('1234')
        )
        return user

    @pytest.fixture
    def create_shop(self, create_user):
        if shop := Shop.objects.first():
            return shop
        shop = Shop.objects.create(
            name="Liz's Shop",
            languages=['en'],
            user=create_user,
            shop_currency=Currency.objects.create(name='USD'),
            shop_category=Category.objects.create(name='ALL')
        )
        return shop

    @pytest.fixture
    def create_product(self, create_shop):
        attributes = [
            {
                "id": 1,
                "price": "700.00",
                "in_stock": True,
                "name": "Standart 123",
                "package_code": None,
                "ikpu_code": None,
                "weight": None,
                "length": None,
                "height": None,
                "width": None
            }
        ]
        product_category = ProductCategory.objects.create(
            name={"en": "Name"},
            description={"en": "Description"}
        )
        product = Product.objects.create(
            name='Product 1',
            description='bla bla bla',
            shop=create_shop,
            category=product_category,
            price='700',
            attributes=attributes
        )
        return product

    @pytest.fixture
    def create_order(self, create_shop, create_product):
        order = Order.objects.create(
            first_name='Elizabeth',
            phone='+1(234)567-8910',
            delivery_type='delivery',
            payment_type='card',
            shop=create_shop
        )
        order.items.add(create_product)
        order.save()
        return order
