from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.views import View
from django.shortcuts import redirect, render
from .blockchain import get_address_details, get_wallets_details
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

        if not "error" in details:
            address = Address.objects.filter(public_key=public_key, user=user)

            if address.exists():
                messages.info(
                    request,
                    mark_safe(f"Wallet <code>{public_key}</code> is already imported."),
                )
            else:
                if len(public_key) == 42:
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
                    messages.error(request, "Incorrect wallet public key.")
        else:
            messages.error(
                request, mark_safe(f"Wallet <code>{public_key}</code> not found.")
            )

        return render(request, "tracker/connect-wallet.html", self.create_context())

    def create_context(self):
        context = {}
        return context


class Balance(View):
    def get(self, request):
        wallets = get_wallets_details(request.user)
        return render(
            request, "tracker/view-holdings.html", self.create_context(wallets)
        )

    def post(self, request):
        return render(request, "tracker/view-holdings.html", self.create_context())

    def create_context(self, wallets):
        context = {"wallets": wallets}
        return context
