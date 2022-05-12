import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import Client

from account.models import User
from tracker.models import Address


class TestTrackerViews:
    def setup_method(self):
        self.client = Client()
        self.credentials = {
            "username": "Test",
            "email": "test@coinspace.com",
            "password": "t8VhtmOUpYJ39Tb0",
        }
        self.user = User.objects.create(
            username=self.credentials["username"],
            email=self.credentials["email"],
            password=self.credentials["password"],
        )
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
        self.holdings_url = reverse("view-holdings")
        self.connect_wallet_url = reverse("connect-wallet")

    @pytest.mark.django_db
    def test_user_tracker_page_access(self):
        response = self.client.get(self.tracker_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_holdings_page_access(self):
        self.client.force_login(self.user)
        response = self.client.get(self.holdings_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_page_access(self):
        response = self.client.get(self.connect_wallet_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_correct_key(self):
        path = reverse("connect-wallet"), self.wallet
        response = self.client.post(path)
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert (
            str(messages[0])
            == "Wallet 0x09a9fd2043e4c1ce330903abd73a3ddda970418c successfully connected!"
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_unexist_key(self):
        path = reverse("connect-wallet"), self.wallet_not_found
        response = self.client.post(path)
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert (
            str(messages[0])
            == "Wallet 000000000000000000000000000000000000000000 not found."
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_incorrect_key(self):
        path = reverse("connect-wallet"), self.wallet_incorrect
        response = self.client.post(path)
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == "Incorrect wallet public key."
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_view_holdings(self):
        self.client.force_login(self.user)
        Address.objects.create(
            label=self.wallet["label"],
            public_key=self.wallet["public-key"],
            user=self.user,
        )
        response = self.client.get(self.holdings_url)
        assert response.context["wallets"][0].label == "Test"
