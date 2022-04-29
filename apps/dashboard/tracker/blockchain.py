import os, requests
from .models import Address

BASE_URL = "https://api.etherscan.io/api"
CMC_URL = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
BLOCKCHAINS = {
    "Ethereum": {
        "name": "Ethereum",
        "symbol": "ETH",
        "decimals": 18,
        "url": "https://api.etherscan.io/api",
        "api_key": os.environ["ETHERSCAN_API_KEY"],
    },
    "Polygon": {
        "name": "Polygon",
        "symbol": "MATIC",
        "decimals": 18,
        "url": "https://api.polygonscan.com/api",
        "api_key": os.environ["POLYGONSCAN_API_KEY"],
    },
    "Avalanche": {
        "name": "Avalanche",
        "symbol": "AVAX",
        "decimals": 18,
        "url": "https://api.snowtrace.io/api",
        "api_key": os.environ["SNOWTRACE_API_KEY"],
    },
}


class Details:
    name = None
    symbol = None
    decimals = None
    url = None
    api_key = None
    address = None

    def __init__(self, blockchain, address):
        self.name = BLOCKCHAINS[blockchain]["name"]
        self.symbol = BLOCKCHAINS[blockchain]["symbol"]
        self.decimals = BLOCKCHAINS[blockchain]["decimals"]
        self.url = BLOCKCHAINS[blockchain]["url"]
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
        return requests.get(self.url, params).json()

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
        result = requests.get(self.url, params).json()
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
                result = requests.get(self.url, params).json()
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


class Wallet:
    def __init__(self, label):
        self.label = label
        self.tokens = []


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

    def value(self):
        """Returns tokens value rounded to 2 decimals."""
        return round(float(self.price * self.balance), 2)
