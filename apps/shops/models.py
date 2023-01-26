from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from multiselectfield import MultiSelectField
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


class ShopCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'


class Currency(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Currency'
        verbose_name_plural = 'Shop Currencies'


class Shop(models.Model):
    class Languages(models.TextChoices):
        UZBEK = 'uz', "O'zbek"
        RUSSIAN = 'ru', 'РУССКИЙ'
        ENGLISH = 'en', 'ENGLISH'

    class Delivery(models.TextChoices):
        PICKUP = 'pickup', "Pickup"
        DELIVERY = 'delivery', 'Delivery'

        @property
        def both(self):
            return self.PICKUP, self.DELIVERY

    name = models.CharField(max_length=255)
    languages = MultiSelectField(max_length=15, choices=Languages.choices, min_choices=1)
    user = models.ForeignKey('users.User', models.CASCADE)
    currency = models.ForeignKey('shops.Currency', models.SET_NULL, null=True, blank=True)
    related_category = models.ForeignKey('shops.ShopCategory', models.CASCADE)
    about_us = models.CharField(max_length=1024, null=True, blank=True)
    delivery_price = models.IntegerField('Delivery Price', null=True, blank=True)
    delivery_price_per_km = models.IntegerField('Delivery Price Per KM', null=True, blank=True)
    minimum_delivery_price = models.IntegerField(null=True, blank=True)
    free_delivery = models.BooleanField(null=True, blank=True)
    about_us_image = models.ImageField(upload_to='shops/', null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    # delivery_types = MultiSelectField(max_length=15, choices=Delivery.choices, min_choices=1, default=Delivery.both)❌
    has_terminal = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    started_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    # plan = ArrayField(JSONField(), default=default)❌
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    delivery_terms = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
