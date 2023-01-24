from django.db import models

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)