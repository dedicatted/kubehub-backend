from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from ..models.account_manager import AccountManager


class Account (AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=60,
        unique=True,
        null=True
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        null=True,
    )
    date_joined = models.DateTimeField(
        verbose_name='data joined',
        auto_now_add=True
    )
    last_login = models.DateTimeField(
        verbose_name='last login',
        auto_now=True
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    readonly_fields = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return f'id: {self.id}, email: {self.email}, username: {self.username}, date_joined: {self.date_joined}, ' \
               f'last_login: {self.last_login}, is_active: {self.is_active}, '

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
