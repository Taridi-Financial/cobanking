from django.urls import path

from . import views

urlpatterns = [
    path("adduser", views.add_user, name="adduser"),
]
