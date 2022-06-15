import os, requests
from datetime import datetime

from .models import Address

BASE_URL = "https://api.etherscan.io/api"
CMC_URL = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
BLOCKCHAINS = {
    "Ethereum": {
        "name": "Ethereum",
        "symbol": "ETH",
        "decimals": 18,
        "url": "https://etherscan.io/",
        "api_url": "https://api.etherscan.io/api",
        "api_key": os.environ["ETHERSCAN_API_KEY"],
    },
    "Polygon": {
        "name": "Polygon",
        "symbol": "MATIC",
        "decimals": 18,
        "url": "https://polygonscan.com/",
        "api_url": "https://api.polygonscan.com/api",
        "api_key": os.environ["POLYGONSCAN_API_KEY"],
    },
    "Avalanche": {
        "name": "Avalanche",
        "symbol": "AVAX",
        "decimals": 18,
        "url": "https://snowtrace.io/",
        "api_url": "https://api.snowtrace.io/api",
        "api_key": os.environ["SNOWTRACE_API_KEY"],
    },
}


class Details:
    name = None
    symbol = None
    decimals = None
    url = None
    api_url = None
    api_key = None
    address = None

    def __init__(self, blockchain, address):
        self.name = BLOCKCHAINS[blockchain]["name"]
        self.symbol = BLOCKCHAINS[blockchain]["symbol"]
        self.decimals = BLOCKCHAINS[blockchain]["decimals"]
        self.url = BLOCKCHAINS[blockchain]["url"]
        self.api_url = BLOCKCHAINS[blockchain]["api_url"]
        self.api_key = BLOCKCHAINS[blockchain]["api_key"]
        self.address = address

    def get_transactions(self):
        """Returns 10,000 last transactions."""
        params = {
            "module": "account",
            "action": "tokentx",
            "address": self.address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "apikey": self.api_key,
        }
        return requests.get(self.api_url, params).json()

    def get_transactions_details(self):
        """Returns 10,000 last transactions details."""
        txs = self.get_transactions()
        transactions = []
        for tx in txs["result"]:
            transaction = Transaction()
            transaction.date = tx["timeStamp"]
            transaction.hash = tx["hash"]
            transaction.url = self.url
            transaction.token = tx["tokenName"]
            transaction.sender = tx["from"]
            transaction.receiver = tx["to"]
            transactions.append(transaction)
        return transactions

    def get_tokens(self):
        """Scans each transaction to return tokens owned."""
        txs = self.get_transactions()
        tokens = []
        for tx in txs["result"]:
            token = Token()
            token.name = tx["tokenName"]
            token.symbol = tx["tokenSymbol"]
            token.contract_address = tx["contractAddress"]
            token.decimals = int(tx["tokenDecimal"])
            if not any(t.name == token.name for t in tokens):
                tokens.append(token)
        tokens.append(self.get_token())
        return tokens

    def get_token(self):
        """Returns current blockchain's token details."""
        params = {
            "module": "account",
            "action": "balance",
            "address": self.address,
            "tag": "latest",
            "apikey": self.api_key,
        }
        result = requests.get(self.api_url, params).json()
        token = Token()
        token.name = self.name
        token.symbol = self.symbol
        token.decimals = self.decimals
        token.balance = float(result["result"]) / 10**token.decimals
        return token

    def get_tokens_details(self):
        """Returns tokens owned price and 24hrs change."""
        tokens = self.get_tokens()
        for token in tokens:
            params = {"symbol": token.symbol}
            headers = {"X-CMC_PRO_API_KEY": os.environ["COINMARKETCAP_API_KEY"]}
            result = requests.get(CMC_URL, params, headers=headers).json()
            try:
                token.price = float(
                    result["data"][token.symbol][0]["quote"]["USD"]["price"]
                )
                token.change = float(
                    result["data"][token.symbol][0]["quote"]["USD"][
                        "percent_change_24h"
                    ]
                )
            except KeyError:
                continue
        return tokens

    def get_tokens_balance(self):
        """Returns tokens owned balance."""
        tokens = self.get_tokens_details()
        for token in tokens:
            if token.contract_address:
                params = {
                    "module": "account",
                    "action": "tokenbalance",
                    "address": self.address,
                    "contractaddress": token.contract_address,
                    "tag": "latest",
                    "apikey": self.api_key,
                }
                result = requests.get(self.api_url, params).json()
                token.balance = float(result["result"]) / 10**token.decimals
        return tokens


def get_address_details(address):
    """Returns address details."""
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": os.environ["ETHERSCAN_API_KEY"],
    }
    return requests.get(BASE_URL, params).json()


def get_wallets_details(user):
    """Returns whole wallet details."""
    addresses = Address.objects.filter(user=user)
    wallets = []
    for address in addresses:
        label = address.label if address.label else address.public_key
        wallet = Wallet(label)
        for bc in BLOCKCHAINS:
            d = Details(bc, address.public_key).get_tokens_balance()
            wallet.tokens.extend(d)
        wallet.tokens.sort(key=lambda x: x.name)
        wallets.append(wallet)
    return wallets


def get_transactions_details(user):
    """Returns whole wallet transactions."""
    addresses = Address.objects.filter(user=user)
    wallets = []
    for address in addresses:
        label = address.label if address.label else address.public_key
        wallet = Wallet(label)
        for bc in BLOCKCHAINS:
            d = Details(bc, address.public_key).get_transactions_details()
            wallet.transactions.extend(d)
        wallet.transactions.sort(key=lambda x: x.date, reverse=True)
        wallets.append(wallet)
    return wallets


class Wallet:
    def __init__(self, label):
        self.label = label
        self.tokens = []
        self.transactions = []


class Token:
    name = None
    symbol = None
    contract_address = None
    decimals = None
    balance = None
    price = None
    change = None

    def pl(self):
        """Returns 24hrs change rounded to 2 decimals."""
        return round(float(self.change), 2)

    def pl_pos(self):
        """Returns True if 24hrs change is positive, False otherwise."""
        return False if "-" in str(self.change) else True

    def get_value(self):
        """Returns token value rounded to 2 decimals."""
        return round(float(self.price * self.balance), 2)

    def get_balance(self):
        """Returns token balance rounded to 8 decimals."""
        return round(float(self.balance), 8)

    def get_price(self):
        """Returns token price rounded to 8 decimals."""
        return round(float(self.price), 8)


class Transaction:
    date = None
    hash = None
    url = None
    token = None
    sender = None
    receiver = None

    def get_date(self):
        """Returns converted timestamp to date."""
        return datetime.fromtimestamp(int(self.date))

    def get_transaction_url(self):
        """Returns transaction URL."""
        return self.url + "tx/" + self.hash

    def get_sender_url(self):
        """Returns transaction URL."""
        return self.url + "address/" + self.sender

    def get_receiver_url(self):
        """Returns transaction URL."""
        return self.url + "address/" + self.receiver
