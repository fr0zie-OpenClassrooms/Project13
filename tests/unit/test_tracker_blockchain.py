import pytest, requests
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import Client
from unittest.mock import Mock

import tracker.blockchain as script


class TestTrackerBlockchain:
    def setup_method(self):
        self.client = Client()

    def test_mock(self, monkeypatch):
        def get(url, params):
            values = [{}]
            mock = Mock()
            mock.json.side_effect = values
            return mock

        monkeypatch.setattr(requests, "get", get)
        self.details = script.Details(
            "Ethereum", "0x09a9fd2043e4c1ce330903abd73a3ddda970418c"
        )
        assert 0
