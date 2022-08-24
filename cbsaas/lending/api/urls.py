from django.urls import path

from . import views


urlpatterns = [
    path("apply-loan", views.apply_loan, name="apply_loan"),
    path("repay-loan", views.repay_loan, name="repay_loan"), 
    path("update-repay-loan", views.repay_loan, name="repay_loan"), 
    path("view-loans", views.repay_loan, name="repay_loan"), 

    path("create-loan-product", views.create_loan_product, name="create_loan_product"),
    path("add-loan-product-charge", views.add_loan_product_charge, name="add_loan_product_charge"),
]
