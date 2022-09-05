from django.urls import path

from . import views

urlpatterns = [
    path("add-payment-dtls", views.add_payment_dtls, name="add_payment_dtls"),
]
