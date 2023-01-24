from django.contrib.auth.models import AbstractUser
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# Create your models here.
class User(AbstractUser, MPTTModel):
    default_shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, null=True, blank=True)
    invitation_token = models.CharField(max_length=255, null=True)
    invitation = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')