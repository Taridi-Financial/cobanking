from django.urls import resolve
from django.contrib.auth import get_user_model

from cbsaas.clients.models import Clients
from cbsaas.clients.services.client_services import get_client_from_ref 
User = get_user_model()

class ClientAuthority:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        return response

    def process_request(self, request):
        user = request.user
        client_ref = request.headers.get("client_ref", None)
        if not client_ref:
            raise 404
        if not (user and user.is_authenticated()):
            raise 403

        client_pk = get_client_from_ref(client_ref, only_pk=True)
        if not User.client_id == client_pk:
            raise 403
        return None