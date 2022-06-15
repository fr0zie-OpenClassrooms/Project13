from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.username

    def hidden_email(self):
        name, host = self.email.split("@")
        name = name[:2] + 4 * "*"
        return "@".join([name, host])

    class Meta:
        app_label = "account"
