from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("add-client", views.add_new_client, name="addclient"),
    path("view-client/<int:client_id>", views.vvvview_client, name="viewclient"),
]
