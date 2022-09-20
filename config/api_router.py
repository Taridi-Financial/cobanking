from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from cbsaas.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

app_name = "api router"
urlpatterns = router.urls

urlpatterns += [
    # API base url
    path("theusers/", include("cbsaas.users.urls")),
    path("ausers/", include("cbsaas.users.api.urls")),
    path("clients/", include("cbsaas.clients.api.urls")),
    path("parameters/", include("cbsaas.parameters.api.urls")),
    path("cb/", include("cbsaas.banking.api.urls")),
    path("lending/", include("cbsaas.lending.api.urls")),
    path("payments/", include("cbsaas.payments.api.urls")),
    path("payments-service/", include("cbsaas.payments_service.api.urls")),
]
