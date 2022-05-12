from django.urls import reverse, resolve


class TestTrackerURLs:
    def test_home(self):
        url = reverse("tracker")
        assert resolve(url).route == "dashboard/tracker/"

    def test_connect_wallet(self):
        url = reverse("connect-wallet")
        assert resolve(url).route == "dashboard/tracker/connect-wallet"

    def test_view_holdings(self):
        url = reverse("view-holdings")
        assert resolve(url).route == "dashboard/tracker/holdings"
