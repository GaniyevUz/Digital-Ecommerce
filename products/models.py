from django.db import models

# Create your models here.
from django.db.models import CharField, TextField, ForeignKey, CASCADE, ImageField, IntegerField, BooleanField
import uuid


class Category(models.Model):
    name = CharField(max_length=255)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=255)
    description = TextField()
    category = ForeignKey('products.Category', on_delete=CASCADE)
    image = ImageField(upload_to='products')
    price = IntegerField()
    in_availability = BooleanField(default=True)
