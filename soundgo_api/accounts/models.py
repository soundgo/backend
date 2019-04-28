from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from .managers import UserAccountManager

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class UserAccount(AbstractBaseUser):

    nickname = models.CharField('Nickname', max_length=255, blank=False, unique=True)
    active = models.BooleanField('Active', default=True)
    admin = models.BooleanField('Admin', default=False)

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    class Meta:
        db_table = 'user_account'
        verbose_name = 'User account'
        verbose_name_plural = 'Users accounts'

    def __str__(self):
        return "%s" % self.nickname

    def get_full_name(self):
        return "%s" % self.nickname

    def get_short_name(self):
        return "%s" % self.nickname

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.admin

    @property
    def is_admin(self):
        return self.admin


class Actor(models.Model):

    user_account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actor',
                                        verbose_name='User account')

    photo = models.CharField('Photo', max_length=800, blank=True)
    email = models.EmailField('Email', max_length=255, blank=False, unique = True)
    minutes = models.PositiveIntegerField('Minutes (s)', default=300)
    credit_card = models.ForeignKey("CreditCard", on_delete=models.SET_NULL, null = True, blank= True, related_name='actor')

    class Meta:
        db_table = 'actor'
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

    def __str__(self):
        return "%s" % self.email


class CreditCard(models.Model):

    holderName = models.CharField(blank=False, max_length=255)
    brandName = models.CharField(blank=False, max_length=255)
    number = models.CharField(blank=False, max_length=255)
    expirationMonth = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    expirationYear = models.PositiveIntegerField()
    cvvCode = models.IntegerField()
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'credit_card'
        verbose_name = 'Credit card'
        verbose_name_plural = 'Credit cards'
