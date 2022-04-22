import requests
from django.shortcuts import render

BASE_URL = "https://api.ethplorer.io/getAddressInfo/"


def tracker(request):
    return render(request, "tracker/tracker.html")


def connect_wallet(request):
    context = {}

    if request.method == "POST":
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

    return render(request, "tracker/connect-wallet.html", context)
