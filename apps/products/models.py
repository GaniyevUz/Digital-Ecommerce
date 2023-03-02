from django.contrib.postgres.fields import ArrayField
from django.db.models import TextChoices, CharField, ForeignKey, TextField, CASCADE, ImageField, BooleanField, \
    IntegerField, JSONField, Model
from mptt.models import MPTTModel, TreeForeignKey

from shared.django import category_directory_path, product_directory_path


class Category(MPTTModel):
    class Translate:
        def __new__(self, *args, **kwargs):
            return {'en': '', 'ru': '', 'uz': ''}

    name = JSONField(default=Translate)
    description = JSONField(default=Translate)
    parent = TreeForeignKey('self', CASCADE, 'children', null=True, blank=True)
    emoji = CharField(max_length=50, null=True, blank=True)
    image = ImageField(upload_to=category_directory_path, null=True, blank=True)
    shop = ForeignKey('shops.Shop', CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name.get('en', '') if hasattr(self.name, 'get') else self.name

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
    image = ImageField(upload_to=product_directory_path, null=True, blank=True)
    price = CharField(max_length=255)
    in_availability = BooleanField(default=True)
    length = CharField(max_length=50, null=True, blank=True)
    width = CharField(max_length=50, null=True, blank=True)
    height = CharField(max_length=50, null=True, blank=True)
    weight = IntegerField(null=True, blank=True)
    length_class = CharField(max_length=10, choices=Length.choices, null=True, blank=True)
    weight_class = CharField(max_length=10, choices=Weight.choices, null=True, blank=True)
    attributes = ArrayField(JSONField())

    @property
    def image_url(self):
        try:
            url = self.image.url
        except (ValueError, AttributeError):
            url = ''
        return url
