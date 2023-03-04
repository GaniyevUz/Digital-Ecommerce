from django.db.models import Model, TextChoices, CharField, ForeignKey, TextField, CASCADE, BooleanField, \
    ManyToManyField, DateTimeField, IntegerField, Manager

from shops.models import Shop


class PaidOrderManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(paid=True)


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
    items = ManyToManyField('products.Product', through='orders.ProductOrder')
    phone = CharField(max_length=225)
    delivery_type = CharField(max_length=225, choices=Shop.Delivery.choices)
    status = CharField(max_length=225, choices=Status.choices, default='in_process')
    payment_type = CharField(max_length=225, default='cash', choices=Payment.choices)
    note = TextField(null=True, blank=True)
    promo_code = CharField(max_length=225, null=True, blank=True)
    paid = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    shop = ForeignKey('shops.Shop', CASCADE)

    objects = Manager()
    paid_objects = PaidOrderManager()

    def __str__(self):
        return self.phone

    class Meta:
        ordering = ('-id',)


class ProductOrder(Model):
    order = ForeignKey('orders.Order', CASCADE)
    product = ForeignKey('products.Product', CASCADE)
    count = IntegerField(default=1)

    class Meta:
        ordering = ('-id',)
