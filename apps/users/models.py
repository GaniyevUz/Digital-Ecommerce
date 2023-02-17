from django.contrib.auth.models import AbstractUser
from django.db.models import OneToOneField, CharField, ForeignKey, SET_NULL, CASCADE


class User(AbstractUser):
    default_shop = OneToOneField('shops.Shop', CASCADE, related_name='default_shop', null=True,
                                 blank=True)
    invitation_token = CharField(max_length=255, null=True)
    invitation = ForeignKey('self', on_delete=SET_NULL, null=True, blank=True)
