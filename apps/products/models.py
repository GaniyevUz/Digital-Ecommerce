from django.contrib.postgres.fields import ArrayField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from shared.model_configs import category_directory_path, product_directory_path


class Category(MPTTModel):
    class Translate:
        def __call__(self, *args, **kwargs):
            return {'en': '', 'ru': '', 'uz': ''}

    name = models.JSONField(default=Translate)
    description = models.JSONField(default=Translate)
    parent = TreeForeignKey('self', models.CASCADE, 'children', null=True, blank=True)
    emoji = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to=category_directory_path, null=True, blank=True)
    shop = models.ForeignKey('shops.Shop', models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name.get('en', '') if hasattr(self.name, 'get') else self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    class Length(models.TextChoices):
        M = 'm', 'Metre'
        CM = 'cm', 'CM'

    class Weight(models.TextChoices):
        KG = 'kg', 'KG'
        GRAM = 'gram', 'Gram'

    name = models.CharField(max_length=255)
    description = models.TextField()
    shop = models.ForeignKey('shops.Shop', models.CASCADE)
    category = models.ForeignKey('products.Category', models.CASCADE)
    image = models.ImageField(upload_to=product_directory_path, null=True, blank=True)
    price = models.CharField(max_length=255)
    in_availability = models.BooleanField(default=True)
    length = models.CharField(max_length=50, null=True, blank=True)
    width = models.CharField(max_length=50, null=True, blank=True)
    height = models.CharField(max_length=50, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    length_class = models.CharField(max_length=10, choices=Length.choices, null=True, blank=True)
    weight_class = models.CharField(max_length=10, choices=Weight.choices, null=True, blank=True)
    attributes = ArrayField(models.JSONField())

    @property
    def image_url(self):
        try:
            url = self.image.url
        except (ValueError, AttributeError):
            url = ''
        return url
