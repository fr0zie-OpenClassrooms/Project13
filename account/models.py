from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

    def hidden_email(self):
        name, host = self.email.split("@")
        name = name[:2] + 4 * "*"
        return "@".join([name, host])

    class Meta:
        app_label = "account"
