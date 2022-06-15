import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import Client

from account.models import User
from tracker.models import Address


class TestTrackerViews:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create(
            username="Test",
            email="test@coinspace.com",
            password="t8VhtmOUpYJ39Tb0",
        )
        self.wallet = {
            "label": "Test",
            "public-key": "0x09a9fd2043e4c1ce330903abd73a3ddda970418c",
        }
        self.wallet_not_found = {
            "label": "Test",
            "public-key": "0x09a9fd2043e4c1ce3309",
        }
        self.wallet_incorrect = {
            "label": "Test",
            "public-key": "0",
        }
        self.tracker_url = reverse("tracker")
        self.holdings_url = reverse("view-holdings")
        self.transactions_url = reverse("view-transactions")
        self.connect_wallet_url = reverse("connect-wallet")

    @pytest.mark.django_db
    def test_user_tracker_page_access(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tracker_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_holdings_page_access(self):
        self.client.force_login(self.user)
        response = self.client.get(self.holdings_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_page_access(self):
        self.client.force_login(self.user)
        response = self.client.get(self.connect_wallet_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_correct_key(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("connect-wallet"), self.wallet)
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert (
            str(messages[0])
            == "Wallet <code>0x09a9fd2043e4c1ce330903abd73a3ddda970418c</code> successfully connected!"
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_unexist_key(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("connect-wallet"), self.wallet_not_found)
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert (
            str(messages[0])
            == "Address <code>0x09a9fd2043e4c1ce3309</code> does not exists."
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_connect_wallet_incorrect_key(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("connect-wallet"), self.wallet_incorrect)
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert (
            str(messages[0]) == "Address <code>0</code> is an invalid address format."
        )
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

    @pytest.mark.django_db
    def test_user_view_transactions(self):
        self.client.force_login(self.user)
        Address.objects.create(
            label=self.wallet["label"],
            public_key=self.wallet["public-key"],
            user=self.user,
        )
        response = self.client.get(self.transactions_url)
        assert response.context["wallets"][0].label == "Test"
