from django.contrib.postgres import fields
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _


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

    class Plans(models.Choices):
        WHATSAPP = dict(service="whatsapp", days=0), 'Whatsapp'
        TELEGRAM = dict(service="telegram", days=0), "Telegram"
        WEB = dict(service="web", days=0), "Web"

    class Defaults:
        PICKUP = 'pickup'
        DELIVERY = 'delivery'

        def delivery(self):
            return f"{self.DELIVERY},{self.PICKUP}"

    name = models.CharField(max_length=255)
    languages = fields.ArrayField(models.CharField(max_length=50, choices=Languages.choices))
    user = models.ForeignKey('users.User', models.CASCADE)
    related_category = models.ForeignKey('shops.ShopCategory', models.CASCADE)
    about_us = models.CharField(max_length=1024, null=True, blank=True)
    delivery_price = models.IntegerField('Delivery Price', null=True, blank=True)
    delivery_price_per_km = models.IntegerField('Delivery Price Per KM', null=True, blank=True)
    minimum_delivery_price = models.IntegerField(null=True, blank=True)
    free_delivery = models.BooleanField(null=True, blank=True)
    about_us_image = models.ImageField(upload_to='shops/', null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    delivery_types = fields.ArrayField(models.CharField(max_length=100, choices=Delivery.choices),
                                       default=Defaults().delivery)
    has_terminal = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    # current_plans = fields.ArrayField(fields.JSONField(choices=Plans.choices))
    # delivery_terms
    lon = models.IntegerField(null=True, blank=True)
    lat = models.IntegerField(null=True, blank=True)
    delivery_terms = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
