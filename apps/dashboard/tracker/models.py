from django.db import models
from django.db.models.deletion import CASCADE

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
    label = models.CharField(max_length=50)
    public_key = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=CASCADE, default=None)
    wallet = models.ForeignKey(Wallet, on_delete=CASCADE, default=None)
    coin = models.ForeignKey(Coin, on_delete=CASCADE, default=None)
