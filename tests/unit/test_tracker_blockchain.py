import requests
from django.test import Client
from unittest.mock import Mock

import tracker.blockchain as script


class TestTrackerBlockchain:
    def setup_method(self):
        self.client = Client()

    def test_get_transactions(self, monkeypatch):
        values = [
            {
                "result": [
                    {
                        "timeStamp": "1651989440",
                        "hash": "0x3d188d6efaa00d18dd5b24c38f80e039c844fd8951092d04dd00de7a30117431",
                        "from": "0x7ae6c1fc4a79129f868f9595fec1a54ff89ff1d2",
                        "to": "0xd1ad24fbb35275049e794687a88b32da93974b56",
                        "tokenName": "APE",
                    },
                ]
            }
        ]
        mock = Mock()
        mock.json.side_effect = values

        def get(url, params):
            return mock

        monkeypatch.setattr(requests, "get", get)
        details = script.Details(
            "Ethereum", "0xD1aD24Fbb35275049E794687A88b32Da93974b56"
        )
        transactions = details.get_transactions_details()
        assert (
            transactions[0].get_transaction_url()
            == "https://etherscan.io/tx/0x3d188d6efaa00d18dd5b24c38f80e039c844fd8951092d04dd00de7a30117431"
        )
        assert (
            transactions[0].get_sender_url()
            == "https://etherscan.io/address/0x7ae6c1fc4a79129f868f9595fec1a54ff89ff1d2"
        )
        assert (
            transactions[0].get_receiver_url()
            == "https://etherscan.io/address/0xd1ad24fbb35275049e794687a88b32da93974b56"
        )
        assert (
            transactions[0].hash
            == "0x3d188d6efaa00d18dd5b24c38f80e039c844fd8951092d04dd00de7a30117431"
        )
        assert transactions[0].token == "APE"

    def test_get_tokens(self, monkeypatch):
        values = [
            {
                "result": [
                    {
                        "contractAddress": "0x3845badade8e6dff049820680d1f14bd3903a5d0",
                        "tokenName": "SAND",
                        "tokenSymbol": "SAND",
                        "tokenDecimal": "18",
                    },
                ]
            },
            {"result": "340395760047161543"},
            {
                "data": {
                    "SAND": [
                        {
                            "quote": {
                                "USD": {
                                    "price": 0.8950706864450875,
                                    "percent_change_24h": 12.2276851,
                                }
                            }
                        }
                    ]
                }
            },
            {},
            {"result": "1000000000000000000000"},
        ]
        mock = Mock()
        mock.json.side_effect = values

        def get(url, params):
            return mock

        monkeypatch.setattr(requests, "get", get)
        details = script.Details(
            "Ethereum", "0xD1aD24Fbb35275049E794687A88b32Da93974b56"
        )
        tokens = details.get_tokens_balance()
        assert tokens[0].name == "SAND"
        assert tokens[0].symbol == "SAND"
        assert (
            tokens[0].contract_address == "0x3845badade8e6dff049820680d1f14bd3903a5d0"
        )
        assert tokens[0].decimals == 18
        assert tokens[0].balance == 1000
        assert tokens[0].price == 0.8950706864450875
        assert tokens[0].pl() == 12.23
        assert tokens[0].pl_pos() is True
