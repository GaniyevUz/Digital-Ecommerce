from django.db.models import Model, TextChoices, CharField, ForeignKey, TextField, CASCADE, BooleanField, \
    ManyToManyField, DateTimeField

from shops.models import Shop


class Order(Model):
    class Status(TextChoices):
        IN_PROCESS = 'in_process', 'In Process'
        READY = 'ready', 'Ready'
        PICKED_UP = 'picked_ip', 'Picked Up'
        REJECTED = 'rejected', 'Rejected'
        DELIVERED = 'delivered', 'Delivered'
        EXPIRED = 'expired', 'Expired'

    class Payment(TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'

    first_name = CharField(max_length=225)
    last_name = CharField(max_length=225, null=True, blank=True)
    items = ManyToManyField('products.Product')
    phone = CharField(max_length=225)
    delivery_type = CharField(max_length=225, choices=Shop.Delivery.choices)
    status = CharField(max_length=225, choices=Status.choices, default='in_process')
    payment_type = CharField(max_length=225, default='cash', choices=Payment.choices)
    note = TextField(null=True, blank=True)
    promo_code = CharField(max_length=225, null=True, blank=True)
    paid = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    shop = ForeignKey('shops.Shop', CASCADE)
