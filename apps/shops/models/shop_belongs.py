from django.contrib.postgres.fields import ArrayField
from django.db.models import Model, CharField, ForeignKey, CASCADE, ImageField, IntegerField, JSONField, BooleanField, \
    DateField, OneToOneField


class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'


class Currency(Model):
    name = CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Currency'
        verbose_name_plural = 'Shop Currencies'


class PaymentProvider(Model):
    code = CharField(max_length=255)
    title = CharField(max_length=255)
    image = ImageField(upload_to='payment_providers/', null=True, blank=True)
    type = CharField(max_length=255)
    status = IntegerField(null=True, blank=True)
    fields = ArrayField(JSONField())
    shop = ForeignKey('shops.Shop', CASCADE)


class TelegramBot(Model):
    token = CharField(max_length=255, unique=True)
    username = CharField(max_length=255, unique=True)
    shop = ForeignKey('shops.Shop', CASCADE)

    def __str__(self):
        return self.username


class Domain(Model):
    name = CharField(max_length=255, unique=True)
    has_ssl = BooleanField(default=True)
    expires_at = DateField(null=True, blank=True)
    is_sub_domain = BooleanField(default=True)
    shop = OneToOneField('shops.Shop', CASCADE)

    def __str__(self):
        return self.name
