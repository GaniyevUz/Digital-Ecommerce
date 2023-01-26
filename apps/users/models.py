from django.contrib.auth.models import AbstractUser
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# Create your models here.
class User(AbstractUser):
    default_shop = models.OneToOneField('shops.Shop', models.CASCADE, related_name='default_shop', null=True, blank=True)
    invitation_token = models.CharField(max_length=255, null=True)
    invitation = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    # invitation = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
