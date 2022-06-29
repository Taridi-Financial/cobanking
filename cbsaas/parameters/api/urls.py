from django.urls import path

from . import views

urlpatterns = [
    path("holder/", views.holder, name="holder"),
]
