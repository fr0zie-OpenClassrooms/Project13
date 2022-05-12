from django.urls import reverse, resolve


class TestHomeURLs:
    def test_profile(self):
        url = reverse("home")
        assert resolve(url).route == ""
