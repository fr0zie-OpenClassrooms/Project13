from django.urls import reverse, resolve


class TestAccountURLs:
    def test_profile(self):
        url = reverse("profile")
        assert resolve(url).route == "account/profile"

    def test_login(self):
        url = reverse("login")
        assert resolve(url).route == "account/login"

    def test_logout(self):
        url = reverse("logout")
        assert resolve(url).route == "account/logout"

    def test_register(self):
        url = reverse("register")
        assert resolve(url).route == "account/register"

    def test_recover_password(self):
        url = reverse("recover-password")
        assert resolve(url).route == "account/recover-password"

    def test_confirm_mail(self):
        url = reverse("confirm-mail")
        assert resolve(url).route == "account/confirm-mail"
