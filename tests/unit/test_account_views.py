import pytest, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.urls import reverse
from django.test import Client

from account.forms import LoginForm, RegistrationForm
from account.models import User


class TestAccountViews:
    def setup_method(self):
        self.client = Client()
        self.credentials = {
            "username": "Test",
            "email": "test@coinspace.com",
            "password1": "t8VhtmOUpYJ39Tb0",
            "password2": "t8VhtmOUpYJ39Tb0",
        }
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    @pytest.mark.django_db
    def test_user_registration_form(self):
        form = RegistrationForm(data=self.credentials)
        assert form.is_valid() == True

    @pytest.mark.django_db
    def test_user_registration_page_access(self):
        response = self.client.get(self.register_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_registration(self):
        response = self.client.post(
            self.register_url, self.credentials, format="text/html"
        )
        user = User.objects.get(
            username=self.credentials["username"],
        )
        assert response.status_code == 302
        assert user.is_authenticated == True

    @pytest.mark.django_db
    def test_user_login_page_access(self):
        response = self.client.get(self.login_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_login(self):
        user = User.objects.create(
            username=self.credentials["username"],
            email=self.credentials["email"],
            password=self.credentials["password1"],
        )
        response = self.client.post(
            self.login_url, self.credentials, format="text/html"
        )
        assert response.status_code == 302
        assert user.is_authenticated == True
