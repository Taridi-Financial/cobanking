from django.urls import path

from . import views

urlpatterns = [
    path("test-disbursment", views.test_disbursment, name="test_disbursment"),
]
