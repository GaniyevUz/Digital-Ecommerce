from django.db import models


class ShopCategory(models.Model):
    name = models.CharField(max_length=255)


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', models.CASCADE)
    shop_category = models.ForeignKey('shops.ShopCategory', models.CASCADE)
