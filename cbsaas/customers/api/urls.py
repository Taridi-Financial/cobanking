from django.urls import path

from . import views

urlpatterns = [ 
    path("add-customer", views.add_customer, name="add_customer"),
    path("update-customer", views.update_customer, name="update_customer"),
    path("approve-customer", views.approve_customer, name="approve_customer"),
    path("delete-customer", views.delete_customer, name="delete_customer"),
    path("view-all-customers", views.view_all_customers, name="view_all_customers"),
    path("view-pending-customers-all", views.view_pending_customers, name="view_pending_customers_all"),
    path("view-pending-customer/<int:id>", views.view_pending_customer, name="view_pending_customers"),
]
