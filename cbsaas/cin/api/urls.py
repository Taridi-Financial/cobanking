from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("add-cin", views.view_cin, name="view_cin"),
    path("view-cin", views.view_cin, name="view_cin"),
    path("view-all-cins", views.view_all_cin, name="view_all_cin"),
    # path("delete-cin/", view=user_update_view, name="update"),
]
