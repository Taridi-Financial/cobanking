from django.urls import path

from . import views

urlpatterns = [ 
    path("add-wallet", views.add_wallet, name="add_wallet"),
    path("edit-wallet", views.edit_wallet, name="edit_wallet"),
    path("delete-wallet", views.delete_wallet, name="delete_wallet"),
    path("view-wallet/<str:waller_ref>", views.view_wallet, name="view_wallet"),
    path("view-wallets", views.view_wallets, name="view_wallets"),
    path("wallet-lookup/<str:waller_ref>", views.wallet_records_lookup, name="wallet_records_lookup"),

    path("view-all-ledgers", views.view_all_ledgers, name="view_all_ledgers"),
    # path("deposit", views.add_ledger, name="add_ledger"),
    # path("transaction-view", views.add_ledger, name="add_ledger"),
]
