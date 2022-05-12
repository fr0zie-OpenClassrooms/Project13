import pytest

from account.models import User


class TestAccountModels:
    @pytest.mark.django_db
    def setup_method(self):
        User.objects.create_user(
            username="Test",
            email="test@coinspace.com",
            password="t8VhtmOUpYJ39Tb0",
        )

    @pytest.mark.django_db
    def test_get_user_by_email(self):
        user = User.objects.get(email="test@coinspace.com")
        assert user.username == "Test"

    @pytest.mark.django_db
    def test_get_user_by_username(self):
        user = User.objects.get(username="Test")
        assert user.email == "test@coinspace.com"

    @pytest.mark.django_db
    def test_get_user_hidden_email(self):
        user = User.objects.get(username="Test")
        assert user.hidden_email() == "te****@coinspace.com"
