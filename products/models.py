from django.db import models

# Create your models here.
from django.db.models import CharField, TextField, ForeignKey, CASCADE, ImageField, IntegerField, BooleanField
import uuid


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=255)
    description = TextField()
    category = ForeignKey('shops.Category', on_delete=CASCADE)
    image = ImageField(upload_to='products/%M')
    price = IntegerField()
    in_availability = BooleanField(default=True)
