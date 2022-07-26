from django.urls import path

from . import views

urlpatterns = [
    path("add-wallet-for-code", views.add_wallet_for_code, name="holder"),
]
