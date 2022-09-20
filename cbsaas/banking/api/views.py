from cbsaas.banking.tasks import celery_test_print
from cbsaas.ibase.services.authorities import has_view_rights
from cbsaas.ibase.services.helpers import format_response, tenant_get_model
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from cbsaas.banking.api.serializers import AddWalletSerializer, WalletAllSerializer, WalletRecordsAllSerializer, TransactionsAllSerializer
from cbsaas.banking.models import Wallet, WalletRecords, Transactions
from cbsaas.banking.services.operations import create_wallet, get_transaction,  wallet_search
from cbsaas.clients.models import Clients
from drf_spectacular.utils import extend_schema


@api_view(['GET', 'POST'])
def wallet_list_or_create(request):
    client_id = request.data.get("client_id", None)
    if request.method == "GET":
        status = request.GET.get('status', None)
        if not status:
            wallet_qs = Wallet.objects.tenant_querry(client_id=client_id).all().order_by("-id")
        else:
            wallet_qs = Wallet.objects.tenant_querry(client_id=client_id).filter(status=status).order_by("-id")
        wallet_serializers = WalletAllSerializer(wallet_qs, many=True)
        return format_response(code=200, message={"wallets":wallet_serializers.data})
    else:
        wallet_serializer = AddWalletSerializer(data=request.data)
        if not wallet_serializer.is_valid():
            return format_response(code=400, message=wallet_serializer.errors)
        
        client_ref=wallet_serializer.data['client_ref']
        wallet_name=wallet_serializer.data['wallet_name']
        wallet_type=request.data['wallet_type']
        scheme_code=wallet_serializer.data['scheme_code']
        create_wlt_resp = create_wallet(client_ref=client_ref, wallet_name=wallet_name, wallet_type=wallet_type)

        action_status = create_wlt_resp["status"]
        message = create_wlt_resp["message"]
        wallet_ref = create_wlt_resp["wallet_ref"]
        if action_status == 1:
            return format_response(code=400, message={"message": message})      
        else:
            return format_response(code=200, message={"status": action_status, "message": message ,"wallet_ref": wallet_ref})


@api_view(['GET', 'PUT', 'DELETE'])
def wallet_get_or_update(request, pk):
    client_id = request.data.get("client_id", None)
    wallet = tenant_get_model(client_id=client_id, pk=pk, model_name="wallet")
    if not wallet:
        return format_response(code=400, message={"message": "Wallet not found"})

    if request.method == "GET":
        wlt_serializer = WalletAllSerializer(wallet)
        return format_response(code=200, message=wlt_serializer.data)

    if request.method == "PUT":
        serializer = AddWalletSerializer(data=request.data)
        wlt_serializer = AddWalletSerializer(instance=wallet, data=request.data)
        if not wlt_serializer.is_valid():
            return format_response(code=400, message=wlt_serializer.errors)
        wlt_serializer.save()
        return format_response(code=200, message=wlt_serializer.data)

    if request.method == "DELETE":
        wallet.delete()
        return format_response(code=204, message={'msg': 'done'})

    
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def wallet_transactions(request):
    client_id = request.data.get("client_id", None)
    waller_ref = request.data.get("waller_ref", None)
    search_rslt = wallet_search(wallet_ref=waller_ref, return_wallet=True)
    if not search_rslt['status'] == 0:
        return format_response(code=400, message={"message": search_rslt["message"]})
    else:
        wallet = search_rslt["wallet"]
        wlt_serializer = WalletAllSerializer(wallet)
        records = WalletRecords.objects.tenant_querry(client_id=client_id).filter(wallet_id=wallet.id).order_by("-id")
        records_serializer = WalletRecordsAllSerializer(records, many=True)
        return format_response(code=200, message={'wlt_dtls': wlt_serializer.data, 'records_dtls': records_serializer.data})

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def transaction_view(request):
    client_id = request.data.get("client_id", None)
    transaction_ref = request.data.get('transaction_ref')
    transaction = get_transaction(client_id=client_id, trans_ref=transaction_ref)
    if not transaction:
        return format_response(code=400, message={"message": "Transaction does not exist"})

    transaction = Transactions.objects.get(id=1)
    trans_serializer = TransactionsAllSerializer(transaction)
    records = WalletRecords.objects.tenant_querry(client_id=client_id).filter(transaction_ref=transaction_ref).order_by("-id")
    records_serializer = WalletRecordsAllSerializer(records, many=True)

    return Response({'transaction': trans_serializer.data, "part_trans":records_serializer.data},
                    status=HTTP_200_OK)

@api_view(["POST"])
def withdraw_funds(request):
    pass

@api_view(["POST"])
def deposit_funds(request):
    pass


@api_view(["POST"])
def transfer_funds(request):
    pass