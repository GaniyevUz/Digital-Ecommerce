from django.db.models import Model, CharField, EmailField, TextChoices, ForeignKey, CASCADE, BooleanField, DateField, \
    DateTimeField


class Client(Model):
    class AccountType(TextChoices):
        EMAIL = 'email', 'Email'
        PHONE = 'phone', 'Phone'

    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = EmailField(max_length=150, unique=True)
    password = CharField(max_length=300)
    phone = CharField(max_length=15, null=True, blank=True)
    account_type = CharField(max_length=10, choices=AccountType.choices)
    shop = ForeignKey('shops.Shop', CASCADE)
