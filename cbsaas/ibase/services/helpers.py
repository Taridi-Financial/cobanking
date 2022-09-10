from cbsaas.cin.models import CINRegistry
from cbsaas.clients.models import Clients
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

def format_response(code=None, message=None):
    if code == 400:
        return Response(message, status=HTTP_400_BAD_REQUEST)
    else:
        return Response(message, status=HTTP_200_OK)


def get_model(id, model_name):
    if model_name == "clients":
        try:
            obj = Clients.objects.get(id=id)
        except Exception:
            obj = None
        return obj

def get_cin_from_number(cin_number):

    try:
        obj = CINRegistry.objects.get(cin=cin_number)
    except Exception:
        obj = None
    return obj


def get_client_from_ref(client_ref):
    try:
        obj = Clients.objects.get(client_ref=client_ref)
    except Exception:
        obj = None
    return obj
