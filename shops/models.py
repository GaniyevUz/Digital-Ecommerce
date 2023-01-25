from django.contrib.postgres import fields
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'


class Currency(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Currency'
        verbose_name_plural = 'Shop Currencies'


# Create your models here.
class Shop(models.Model):
    class Languages(models.TextChoices):
        UZBEK = 'uz', "O'zbek"
        RUSSIAN = 'ru', 'РУССКИЙ'
        ENGLISH = 'en', 'ENGLISH'
    name = models.CharField(max_length=255)
    languages = fields.ArrayField(models.CharField(max_length=50, choices=Languages.choices))
    user = models.ForeignKey('users.User', models.CASCADE)
    shop_category = models.ForeignKey('shops.Category', models.CASCADE)
