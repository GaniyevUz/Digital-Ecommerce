from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields

from products.managers import CategoryManager


#
# {
#     'en': 'book',
#     'ru': 'kniga',
#     'uz': 'kitob',
# }


class Category(MPTTModel):
    name = models.JSONField(default=dict)
    description = models.JSONField(default=dict, null=True, blank=True)
    parent = TreeForeignKey('self', models.CASCADE, 'children', null=True, blank=True)
    emoji = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='shop/categories/', null=True, blank=True)
    shop = models.ForeignKey('shops.Shop', models.CASCADE, null=True, blank=True)
    objects = CategoryManager()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    class Length(models.TextChoices):
        M = 'm', 'Metre'
        CM = 'cm', 'CM'

    class Weight(models.TextChoices):
        KG = 'kg', 'KG'
        GRAM = 'gram', 'Gram'

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey('products.Category', models.CASCADE)
    image = models.ImageField(upload_to='products/%m', null=True, blank=True)
    price = models.IntegerField()
    in_availability = models.BooleanField(default=True)

    length = models.CharField(max_length=50, null=True, blank=True)
    width = models.CharField(max_length=50, null=True, blank=True)
    height = models.CharField(max_length=50, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    length_class = models.CharField(max_length=10, choices=Length.choices, null=True, blank=True)
    weight_class = models.CharField(max_length=10, choices=Weight.choices, null=True, blank=True)
