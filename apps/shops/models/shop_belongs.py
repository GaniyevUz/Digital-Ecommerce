from django.db.models import Model, CharField, ForeignKey, CASCADE, BooleanField, \
    DateField, OneToOneField


class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'
        ordering = ('-id',)


class Currency(Model):
    name = CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Currency'
        verbose_name_plural = 'Shop Currencies'
        ordering = ('-id',)


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


class Country(Model):
    name = CharField(max_length=255, unique=True)
