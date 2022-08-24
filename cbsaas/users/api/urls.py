from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("adduser", views.add_user, name="adduser"),
    # path("login", views.login, name="adduser"),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
