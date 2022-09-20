from cbsaas.banking.api.serializers import WalletAllSerializer
from cbsaas.banking.models import Wallet
from cbsaas.clients.services.consumer_services import consumers_create_consumer, consumers_get_or_check_sn
from cbsaas.ibase.services.helpers import format_response, get_model, tenant_get_model
from cbsaas.lending.api.serializers import LoanAllSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from ..models import  Branches, ConsumerRegistry
from .serializers import BranchViewSerializer, BranchEditSerializer, ClientsAddSerializer, ClientsAllSerializer, ClientsUpdateSerializer, ConsumerEditSerializer, ConsumerViewSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_new_client(request):
    serializer = ClientsAddSerializer(data=request.data)
    if serializer.is_valid():
        client_name = serializer.data.get("client_name")
        address = serializer.data.get("address")
        identifying_number = serializer.data.get("identifying_number")

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_client(request, client_id):
    client = get_model(client_id, "clients")
    if not client:
        return format_response(code=400, message="Client not found")
    serializer = ClientsAllSerializer(client)
    return format_response(code=200, message=serializer.data)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def update_client(request, client_id):
    client = get_model(client_id, "clients")
    if not client:
        return format_response(code=400, message="Client not found")
    serializer = ClientsAddSerializer(instance=client,data=request.data)
    if not serializer.is_valid():
        return format_response(code=400, message=serializer.errors)
    serializer.save()
    return format_response(code=200, message=serializer.errors)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def vvvview_client(request, client_id):
    client = get_model(client_id, "clients")
    if not client:
        return format_response(code=400, message="Client not found")
    serializer = ClientsAllSerializer(client)
    return format_response(code=200, message=serializer.data)

@api_view(['GET', 'POST'])
def branch_list_or_create(request):
    client_id = request.data.get("client_id", None)
    if request.method == "GET":
        status = request.GET.get('status', None)
        if not status:
            branch_qs = Branches.objects.tenant_querry(client_id=client_id).all().order_by("-id")
        else:
            branch_qs = Branches.objects.tenant_querry(client_id=client_id).filter(status=status).order_by("-id")

        branch_serializers = ConsumerViewSerializer(branch_qs, many=True)
        return format_response(code=200, message=branch_serializers.data)
    else:
        branch_serializers = BranchEditSerializer(data=request.data)
        if not branch_serializers.is_valid(raise_exception=True):
            return format_response(code=400, message=branch_serializers.errors)
        branch_serializers.save()
        return format_response(code=201, message=branch_serializers.data)


@api_view(['GET', 'PUT', 'DELETE'])
def branch_get_or_update(request, pk):
    client_id = request.data.get("client_id", None)
    branch = tenant_get_model(client_id=client_id, pk=pk, model_name="branches")
    if not branch:
        return format_response(code=400, message="Branch not found")
    if request.method == "GET":
        branch_serializer = BranchViewSerializer(branch)
        return format_response(code=200, message=branch_serializer.data)
    if request.method == "PUT":
        branch_serializer = BranchEditSerializer(instance=branch, data=request.data)
        branch_serializer.is_valid(raise_exception=True)
        branch_serializer.save()
        return format_response(code=200, message=branch_serializer.data)
    if request.method == "DELETE":
        branch.delete()
        return format_response(code=204, message={'msg': 'done'})


@api_view(['GET', 'POST'])
def consumer_list_or_create(request):
    client_id = request.data.get("client_id", None)
    if request.method == "GET":
        status = request.GET.get('status', None)
        if not status:
            consumer_qs = ConsumerRegistry.objects.tenant_querry(client_id=client_id).all().order_by("-id")
        else:
            consumer_qs = ConsumerRegistry.objects.tenant_querry(client_id=client_id).filter(status=status).order_by("-id")

        consumer_serializers = BranchViewSerializer(consumer_qs, many=True)
        return format_response(code=200, message=consumer_serializers.data)
    else:
        consumer_serializers = ConsumerEditSerializer(data=request.data)
        if not consumer_serializers.is_valid(raise_exception=True):
            return format_response(code=400, message=consumer_serializers.errors)
        consumer_msg = consumers_create_consumer(client_id=None, consumer_national_no=None, owner_type=None)
        if not consumer_msg["status"] == 0:
            return format_response(code=400, message={'msg': consumer_msg["message"]} )
        return format_response(code=200, message=consumer_msg)


@api_view(['GET', 'PUT', 'DELETE'])
def consumer_get_or_update(request, pk):
    client_id = request.data.get("client_id", None)
    consumer = tenant_get_model(client_id=client_id, pk=pk, model_name="consumer")
    if not consumer:
        return format_response(code=400, message="Branch not found")
    if request.method == "GET":
        consumer_serializer = ConsumerViewSerializer(consumer)
        return format_response(code=200, message={'consumer': consumer_serializer.data})
    if request.method == "PUT":
        consumer_serializer = ConsumerEditSerializer(instance=consumer, data=request.data)
        if not consumer_serializer.is_valid(raise_exception=True):
            return format_response(code=400, message=consumer_serializer.errors)
        consumer_serializer.save()
        return format_response(code=200, message=consumer_serializer.data)
    if request.method == "DELETE":
        consumer.delete()
        return format_response(code=204, message={'msg': 'done'})

@api_view(['GET'])
def consumer_get_resources(request, cin_no):
    client_id = request.data.get("client_id", None)
    
    consumer = consumers_get_or_check_sn(
        client_id=client_id, 
        consumer_system_no=cin_no, 
        is_check_rqst=False)

    if not consumer:
        return format_response(code=400, message="Consumer  with that number not found")

    wallet_qs = consumer.wallet_set.all()
    wallet_serializers = WalletAllSerializer(wallet_qs, many=True)

    loan_qs = consumer.loan_set.all()
    loan_serializers = LoanAllSerializer(loan_qs, many=True)
    return format_response(code=200, message={"wallets":wallet_serializers.data,"loans":loan_serializers.data})

