from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields


class Category(MPTTModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Title"), max_length=200),
        description=models.TextField(null=True, blank=True)
    )
    parent = TreeForeignKey('self', models.CASCADE, 'children', null=True, blank=True)
    emoji = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='shop/categories/', null=True, blank=True)
    shop = models.ForeignKey('shops.Shop', models.CASCADE, null=True, blank=True)


class Product(models.Model):
    class Lenght(models.TextChoices):
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
    length_class = models.CharField(max_length=10, choices=Lenght.choices, null=True, blank=True)
    weight_class = models.CharField(max_length=10, choices=Weight.choices, null=True, blank=True)
