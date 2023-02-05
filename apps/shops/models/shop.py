from django.db import models
from multiselectfield import MultiSelectField


class Shop(models.Model):
    class Languages(models.TextChoices):
        UZBEK = 'uz', "O'zbek"
        RUSSIAN = 'ru', 'РУССКИЙ'
        ENGLISH = 'en', 'ENGLISH'

    class Delivery(models.TextChoices):
        PICKUP = 'pickup', "Pickup"
        DELIVERY = 'delivery', 'Delivery'

    name = models.CharField(max_length=255)
    languages = MultiSelectField(max_length=15, choices=Languages.choices, min_choices=1)
    user = models.ForeignKey('users.User', models.CASCADE)
    shop_currency = models.ForeignKey('shops.Currency', models.RESTRICT)
    shop_category = models.ForeignKey('shops.Category', models.RESTRICT)
    delivery_types = MultiSelectField(max_length=15, choices=Delivery.choices, min_choices=1, default=Delivery.PICKUP)
    about_us = models.CharField(max_length=1024, null=True, blank=True)
    delivery_price = models.IntegerField('Delivery Price', null=True, blank=True)
    delivery_price_per_km = models.IntegerField('Delivery Price Per KM', null=True, blank=True)
    minimum_delivery_price = models.IntegerField(null=True, blank=True)
    free_delivery = models.BooleanField(null=True, blank=True)
    about_us_image = models.ImageField(upload_to='shops/', null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    has_terminal = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    # plan = ArrayField(JSONField(), default=default)❌
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    delivery_terms = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def categories(self):
        return self.category_set.all()

    @property
    def orders(self):
        return self.order_set.all()
