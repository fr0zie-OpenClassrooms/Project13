from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views import View
from django.shortcuts import redirect, render
from .blockchain import (
    get_address_details,
    get_wallets_details,
    get_transactions_details,
)
from .models import Address


class Tracker(View):
    def get(self, request):
        return render(request, "tracker/tracker.html")

    def post(self, request):
        return render(request, "tracker/tracker.html")


class ConnectWallet(View):
    def get(self, request):
        return render(request, "tracker/connect-wallet.html", self.create_context())

    def post(self, request):
        user = request.user
        label = request.POST.get("label")
        public_key = request.POST.get("public-key")
        details = get_address_details(public_key)

        if details["status"] == "1":
            address = Address.objects.filter(public_key=public_key, user=user)

            if address.exists():
                messages.info(
                    request,
                    mark_safe(f"Wallet <code>{public_key}</code> is already imported."),
                )
            else:
                if int(details["result"]) > 0:
                    address = Address.objects.create(
                        label=label, public_key=public_key, user=user
                    )
                    messages.success(
                        request,
                        mark_safe(
                            f"Wallet <code>{public_key}</code> successfully connected!"
                        ),
                    )
                else:
                    messages.error(
                        request, f"Address <code>{public_key}</code> does not exists."
                    )
        else:
            messages.error(
                request,
                mark_safe(
                    f"Address <code>{public_key}</code> is an invalid address format."
                ),
            )

        return render(request, "tracker/connect-wallet.html", self.create_context())

    def create_context(self):
        context = {}
        return context


class Holdings(View):
    def get(self, request):
        wallets = get_wallets_details(request.user)
        return render(
            request, "tracker/view-holdings.html", self.create_context(wallets)
        )

    def post(self, request):
        return render(request, "tracker/view-holdings.html", self.create_context(None))

    def create_context(self, wallets):
        context = {"wallets": wallets}
        return context


class Transactions(View):
    def get(self, request):
        wallets = get_transactions_details(request.user)
        return render(
            request, "tracker/view-transactions.html", self.create_context(wallets)
        )

    def post(self, request):
        return render(
            request, "tracker/view-transactions.html", self.create_context(None)
        )

    def create_context(self, wallets):
        context = {"wallets": wallets}
        return context
