from django.db import models

# Create your models here.
from django.db.models import CharField, TextField, ForeignKey, CASCADE, ImageField, IntegerField, BooleanField, \
    TextChoices
import uuid


class Product(models.Model):
    class Lenght(TextChoices):
        M = 'm', 'Metre'
        CM = 'cm', 'CM'

    class Weight(TextChoices):
        KG = 'kg', 'KG'
        GRAM = 'gram', 'Gram'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=255)
    description = TextField()
    category = ForeignKey('shops.Category', on_delete=CASCADE)
    image = ImageField(upload_to='products/%m', null=True, blank=True)
    price = IntegerField()
    in_availability = BooleanField(default=True)

    length = CharField(max_length=50, null=True, blank=True)
    width = CharField(max_length=50, null=True, blank=True)
    height = CharField(max_length=50, null=True, blank=True)
    weight = IntegerField(null=True, blank=True)
    length_class = CharField(max_length=10, choices=Lenght.choices, null=True, blank=True)
    weight_class = CharField(max_length=10, choices=Weight.choices, null=True, blank=True)
