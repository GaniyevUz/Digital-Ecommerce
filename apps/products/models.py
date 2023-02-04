from django.db.models import Model, CharField, JSONField, ImageField, IntegerField, TextField, BooleanField, ForeignKey, CASCADE, TextChoices
from mptt.models import MPTTModel, TreeForeignKey

from products.managers import CategoryManager


class Category(MPTTModel):
    class Translate:
        @staticmethod
        def default_translate():
            return {'en': '', 'ru': '', 'uz': ''}

    name = JSONField(default=Translate().default_translate)
    description = JSONField(default=Translate().default_translate)
    parent = TreeForeignKey('self', CASCADE, 'children', null=True, blank=True)
    emoji = CharField(max_length=50, null=True, blank=True)
    image = ImageField(upload_to='shop/categories/', null=True, blank=True)
    shop = ForeignKey('shops.Shop', CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name.get('en', '')

    class Meta:
        verbose_name_plural = 'Categories'


class Product(Model):
    class Length(TextChoices):
        M = 'm', 'Metre'
        CM = 'cm', 'CM'

    class Weight(TextChoices):
        KG = 'kg', 'KG'
        GRAM = 'gram', 'Gram'

    name = CharField(max_length=255)
    description = TextField()
    category = ForeignKey('products.Category', CASCADE)
    image = ImageField(upload_to='products/%m', null=True, blank=True)
    price = IntegerField()
    in_availability = BooleanField(default=True)

    length = CharField(max_length=50, null=True, blank=True)
    width = CharField(max_length=50, null=True, blank=True)
    height = CharField(max_length=50, null=True, blank=True)
    weight = IntegerField(null=True, blank=True)
    length_class = CharField(max_length=10, choices=Length.choices, null=True, blank=True)
    weight_class = CharField(max_length=10, choices=Weight.choices, null=True, blank=True)
