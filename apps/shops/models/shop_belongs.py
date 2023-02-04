from django.contrib.postgres.fields import ArrayField
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'


class Currency(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Currency'
        verbose_name_plural = 'Shop Currencies'


class PaymentProvider(models.Model):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='payment_providers/', null=True, blank=True)
    type = models.CharField(max_length=255)
    status = models.IntegerField(null=True, blank=True)
    fields = ArrayField(models.JSONField())
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE)
