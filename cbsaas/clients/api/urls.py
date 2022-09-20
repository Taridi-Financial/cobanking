from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("add-client", views.add_new_client, name="addclient"),
    path("view-client/<int:client_id>", views.vvvview_client, name="viewclient"),
    path('branches', views.branch_list_or_create, name="branch_list_or_create"),
    path('branches/<int:pk>/', views.branch_get_or_update, name="branch_get_or_update"),

    path('consumers', views.consumer_list_or_create, name="consumer_list_or_create"),
    path('consumer/<int:pk>/', views.consumer_get_or_update, name="consumer_get_or_update"),
    path('consumer-resources/<str:cin_no>/', views.consumer_get_resources, name="consumer_get_or_update"),
]
