from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import OneToOneField, CharField, ForeignKey, SET_NULL, CASCADE, EmailField, TextChoices


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, username, shop=None):
        return self.get(**{self.model.USERNAME_FIELD: username, 'shop': shop})

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class AccountType(TextChoices):
        EMAIL = 'email', 'Email'
        PHONE = 'phone', 'Phone'

    email = EmailField(max_length=255)
    default_shop = OneToOneField('shops.Shop', CASCADE, related_name='default_shop', null=True,
                                 blank=True)
    invitation_token = CharField(max_length=255, null=True)
    invitation = ForeignKey('self', SET_NULL, null=True, blank=True)
    phone = CharField(max_length=15, null=True, blank=True)
    account_type = CharField(max_length=10, choices=AccountType.choices)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['shop']
    objects = UserManager()
    shop = ForeignKey('shops.Shop', CASCADE, 'shops', null=True, blank=True)  # client for this shop

    class Meta:
        unique_together = ('email', 'shop')
