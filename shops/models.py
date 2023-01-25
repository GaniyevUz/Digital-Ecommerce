from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', models.CASCADE)
    shop_category = models.ForeignKey('shops.Category', models.CASCADE)
