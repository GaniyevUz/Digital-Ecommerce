from django.contrib.postgres.fields import ArrayField
from django.db.models import TextChoices, CharField, ForeignKey, TextField, CASCADE, ImageField, BooleanField, \
    IntegerField, JSONField, Model, RESTRICT, DateTimeField, DecimalField
from multiselectfield import MultiSelectField

from shared.utils import site_languages


class Shop(Model):
    langs = [(lang.get('code'), lang.get('title')) for lang in site_languages]

    class Delivery(TextChoices):
        PICKUP = 'pickup', "Pickup"
        DELIVERY = 'delivery', 'Delivery'

    name = CharField(max_length=255)
    languages = MultiSelectField(max_length=255, choices=langs, min_choices=1)
    user = ForeignKey('users.User', CASCADE, related_name='shops')  # owner of the shop
    shop_currency = ForeignKey('shops.Currency', RESTRICT)
    shop_category = ForeignKey('shops.Category', RESTRICT)
    country = ForeignKey('shops.Country', RESTRICT)
    delivery_types = MultiSelectField(max_length=255, choices=Delivery.choices, min_choices=1, default=Delivery.PICKUP)
    about_us = CharField(max_length=1024, null=True, blank=True)
    delivery_price = IntegerField('Delivery Price', null=True, blank=True)
    delivery_price_per_km = IntegerField('Delivery Price Per KM', null=True, blank=True)
    minimum_delivery_price = IntegerField(null=True, blank=True)
    free_delivery = BooleanField(null=True, blank=True)
    about_us_image = ImageField(upload_to='shops/', null=True, blank=True)
    expires_at = DateTimeField(null=True, blank=True)
    has_terminal = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True, editable=False)
    starts_at = DateTimeField(null=True, blank=True)
    ends_at = DateTimeField(null=True, blank=True)
    current_plans = ArrayField(JSONField(), null=True)
    lon = DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lat = DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    delivery_terms = TextField(null=True, blank=True)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def categories(self):
        return self.category_set.all()

    @property
    def orders(self):
        return self.order_set.all()

    @property
    def clients(self):
        return self.client_set.all()

    @property
    def payment_providers(self):
        return self.paymentprovider_set.all()

    @property
    def telegram_bot(self):
        return self.telegrambot_set.first()

    class Meta:
        ordering = ['-id']
