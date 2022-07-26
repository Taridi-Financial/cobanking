from django.urls import path

from . import views

urlpatterns = [ 
    path("add-ledger", views.add_ledger, name="add_ledger"),
    path("view-all-ledgers", views.view_all_ledgers, name="view_all_ledgers"),
    path("wallet-lookup/<str:waller_ref>", views.wallet_lookup, name="wallet_lookup"),
    path("deposit", views.add_ledger, name="add_ledger"),
]
