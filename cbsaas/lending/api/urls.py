from django.urls import path

from . import views


urlpatterns = [
    path("apply-loan", views.apply_loan, name="apply_loan"),
    path("request-to-repay-loan", views.request_to_repay_loan, name="request_to_repay_loan"), 
    path("manual-repay-loan", views.manual_repay_loan, name="repay_loan"),  
    path("view-loans/<str:client_ref>", views.view_loans, name="view_loans"), 
    path("approve-loan", views.approve_loan, name="approve_loan"), 
    path("add-loan-security", views.add_loan_security, name="add_loan_security"), 

    path("create-loan-product", views.create_loan_product, name="create_loan_product"),
    path("add-loan-product-charge", views.add_loan_product_charge, name="add_loan_product_charge"),
    path("set-unrealized-interest-wallet", views.apply_loan, name="apply_loan"),
]
