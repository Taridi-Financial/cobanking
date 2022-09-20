from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("adduser", views.add_user, name="adduser"),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("members", views.members_list, name="members_list"),
    path('member/<int:pk>/', views.member_get_or_update, name="member_get_or_update"),
]
