from operator import truediv
from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT

from account.models import User


class Type(models.Model):
    name = models.CharField(max_length=50)


class Wallet(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=CASCADE, default=None)


class Coin(models.Model):
    name = models.CharField(max_length=20)
    token = models.CharField(max_length=20)


class Address(models.Model):
    label = models.CharField(max_length=50, default=None, blank=True, null=True)
    public_key = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=CASCADE)
    wallet = models.ForeignKey(
        Wallet, on_delete=SET_DEFAULT, default=None, blank=True, null=True
    )
    coin = models.ForeignKey(
        Coin, on_delete=SET_DEFAULT, default=None, blank=True, null=True
    )
