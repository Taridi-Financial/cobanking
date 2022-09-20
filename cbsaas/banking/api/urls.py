from django.urls import path

from . import views

urlpatterns = [ 
    path('wallet', views.wallet_list_or_create, name="wallet_list_or_create"),
    path('wallet/<int:pk>/', views.wallet_get_or_update, name="wallet_get_or_update"),
    path("wallet-transactions", views.wallet_transactions, name="wallet_transactions"),
    path("transaction-view", views.transaction_view, name="transaction_view"),
    path("withdraw", views.withdraw_funds, name="withdraw_funds"),
    path("deposit", views.deposit_funds, name="deposit_funds"),
    path("transfer-funds", views.transfer_funds, name="transfer_funds"),
    
]
