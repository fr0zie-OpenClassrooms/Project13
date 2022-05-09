import pytest
from django.urls import reverse
from django.test import Client

from tracker.models import Address


class TestTrackerViews:
    def setup_method(self):
        self.wallet = {
            "label": "Test",
            "public-key": "0x09a9fd2043e4c1ce330903abd73a3ddda970418c",
        }
        self.wallet_not_found = {
            "label": "Test",
            "public-key": "000000000000000000000000000000000000000000",
        }
        self.wallet_incorrect = {
            "label": "Test",
            "public-key": "0",
        }
        self.tracker_url = reverse("tracker")
        self.holdings_url = reverse("holdings")
        self.connect_wallet_url = reverse("connect-wallet")

    @pytest.mark.django_db
    def test_user_tracker_page_access(self):
        client = Client()
        response = client.get(self.tracker_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_holdings_page_access(self):
        client = Client()
        response = client.get(self.holdings_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_page_access(self):
        client = Client()
        response = client.get(self.connect_wallet_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_correct_key(self):
        client = Client()
        path = reverse("connect-wallet", kwargs=self.wallet)
        response = client.post(path)
        messages = list(response.context["messages"])
        assert len(messages) == 1
        assert (
            messages[0]
            == "Wallet 0x09a9fd2043e4c1ce330903abd73a3ddda970418c successfully connected!"
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_unexist_key(self):
        client = Client()
        path = reverse("connect-wallet", kwargs=self.wallet_not_found)
        response = client.post(path)
        messages = list(response.context["messages"])
        assert len(messages) == 1
        assert (
            messages[0]
            == "Wallet 000000000000000000000000000000000000000000 not found."
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_incorrect_key(self):
        client = Client()
        path = reverse("connect-wallet", kwargs=self.wallet_incorrect)
        response = client.post(path)
        messages = list(response.context["messages"])
        assert len(messages) == 1
        assert messages[0] == "Incorrect wallet public key."
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_view_holdings(self):
        client = Client()
        wallet = Address.objects.create(
            label=self.wallet["label"],
            public_key=self.wallet["public-key"],
            user=client,
        )
        response = client.get(self.holdings_url)
        assert response.context["wallet-label"] == "Test"
