import requests
from django.views import View
from django.shortcuts import render

BASE_URL = "https://api.ethplorer.io/getAddressInfo/"


class Tracker(View):
    def get(self, request):
        return render(request, "tracker/tracker.html")

    def post(self, request):
        return render(request, "tracker/tracker.html")


class ConnectWallet(View):
    def get(self, request):
        return render(request, "tracker/connect-wallet.html", self.create_context())

    def post(self, request):
        balance = {}
        url = BASE_URL + request.POST.get("public-key")
        params = {"apiKey": "freekey"}
        result = requests.get(url, params).json()

        balance["ETH"] = result["ETH"]["balance"]

        for token in result["tokens"]:
            try:
                token_decimals = int(token["tokenInfo"]["decimals"])
                token_symbol = token["tokenInfo"]["symbol"]
                token_balance = token["balance"] / (10**token_decimals)
                balance[token_symbol] = token_balance
            except:
                continue

        for value in balance:
            print(value + ": " + str(balance[value]))

        return render(request, "tracker/connect-wallet.html", self.create_context())

    def create_context(self):
        context = {}
        return context
