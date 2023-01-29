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
