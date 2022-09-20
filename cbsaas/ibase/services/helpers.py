from cbsaas.cin.models import ConsumerRegistry
from cbsaas.clients.models import Branches, Clients
from rest_framework.response import Response
from rest_framework import status

def format_response(code=None, message=None):
    if code == 400:
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    elif code ==200:
        return Response(message, status=status.HTTP_200_OK)
    elif code ==204:
        return Response(message, status=status.HTTP_204_NO_CONTENT)


def get_model(id, model_name):
    if model_name == "clients":
        try:
            obj = Clients.objects.get(id=id)
        except Exception:
            obj = None
        return obj

def get_cin_from_number(cin_number):

    try:
        obj = ConsumerRegistry.objects.get(cin=cin_number)
    except Exception:
        obj = None
    return obj


def get_client_from_ref(client_ref):
    try:
        obj = Clients.objects.get(client_ref=client_ref)
    except Exception:
        obj = None
    return obj


def tenant_get_model(client_id=None, pk=None, model_name=None):
    if model_name == "branches":
        try:
            obj = Branches.objects.tenant_querry(client_id=client_id).get(id=pk)
        except Exception:
            obj = None
        return obj