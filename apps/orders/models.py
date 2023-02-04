from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from shops.models import Shop


class Order(models.Model):
    class Status(models.TextChoices):
        IN_PROCESS = 'in_process', _('In Process')
        READY = 'ready', _('Ready')
        PICKED_UP = 'picked_ip', _('Picked Up')
        REJECTED = 'rejected', _('Rejected')
        DELIVERED = 'delivered', _('Delivered')
        EXPIRED = 'expired', _('Expired')

    class Payment(models.TextChoices):
        CASH = 'cash', _('Cash')
        CARD = 'card', _('Card')

    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225, null=True, blank=True)
    items = models.ManyToManyField('products.Product')
    phone = models.CharField(max_length=225)
    delivery_type = models.CharField(max_length=15, choices=Shop.Delivery.choices),
    status = models.CharField(max_length=50, choices=Status.choices, default='in_process'),
    payment_type = models.CharField(max_length=225, default='cash', choices=Payment.choices),
    note = models.TextField(null=True, blank=True)
    total_price = models.IntegerField()
    promo_code = models.CharField(max_length=225, null=True, blank=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey('shops.Shop', models.CASCADE)
