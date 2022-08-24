from cbsaas.banking.tasks import celery_test_print
from cbsaas.ibase.services.authorities import has_view_rights
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from cbsaas.banking.api.serializers import AddWalletSerializer, WalletAllSerializer, WalletRecordsAllSerializer, TransactionsAllSerializer
from cbsaas.banking.models import Wallet, WalletRecords, Transactions
from cbsaas.banking.services.operations import create_wallet, get_transaction_details, wallet_search
from cbsaas.clients.models import Clients



@api_view(["POST"])
def move_funds(request):
    transaction = Transactions()
    transaction.transact(debit_wallet_ref=0, credit_wallet_ref=0, amount=0)


@api_view(["POST"])
def deposit_funds(request):
    transaction = Transactions()
    transaction.transact(debit_wallet_ref=0, credit_wallet_ref=0, amount=0)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def add_wallet(request):
    serializer = AddWalletSerializer(data=request.data)
    if serializer.is_valid():
        client_ref=serializer.data['client_ref']
        wallet_name=serializer.data['wallet_name']
        wallet_type=request.data['wallet_type']

        scheme_code=serializer.data['scheme_code']
       
        create_wlt_resp = create_wallet(
            client_ref=client_ref, wallet_name=wallet_name, wallet_type=wallet_type
        )
        action_status = create_wlt_resp["status"]
        message = create_wlt_resp["message"]
        wallet_ref = create_wlt_resp["wallet_ref"]
        if action_status == 1:
            return Response(
                {"status": action_status, "message": message,},
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"status": action_status, "message": message ,"wallet_ref": wallet_ref}, status=HTTP_200_OK
            )

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def edit_wallet(request):
    serializer = AddWalletSerializer(data=request.data)
    if serializer.is_valid():

        wallet_name=serializer.data['wallet_name']
        wallet_type=serializer.data['wallet_type']
        
        wallet_ref=serializer.data['wallet_ref']

        wallet_search =  wallet_search(wallet_ref=wallet_ref, return_wallet=True)
        if not wallet_search["status"] == 0:
            return Response({ "message": wallet_search["message"]},status=HTTP_400_BAD_REQUEST)
        else:
            wallet = wallet_search["wallet"]
            wallet.wallet_name = wallet_name
            wallet.wallet_type = wallet_type
            wallet.save()
            return Response({ "message": "wallet updated successfully" ,"wallet_ref": wallet_ref}, status=HTTP_200_OK)

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_wallet(request, waller_ref):
    search_rslt = wallet_search(wallet_ref=waller_ref, return_wallet=True)
    if search_rslt['status'] == 0:
        
        wallet = search_rslt["wallet"]
        wlt_serializer = WalletAllSerializer(wallet)
        return Response({'wlt_dtls': wlt_serializer.data, },
                status=HTTP_200_OK)   



@api_view(["POST"])
def delete_wallet(request):
    wallet_ref=request.data['wallet_ref']
    search_rslts =  wallet_search(wallet_ref=wallet_ref, return_wallet=True)
    if not search_rslts["status"] == 0:
        return Response({ "message": search_rslts["message"]},status=HTTP_400_BAD_REQUEST)
    else:
        wallet = search_rslts["wallet"]
        wallet.delete()
        return Response({ "message": "wallet updated successfully" ,"wallet_ref": wallet_ref}, status=HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_wallets(request):
    celery_test_print.delay()
    wallets = Wallet.objects.all().order_by("-id")
    serializer = WalletAllSerializer(wallets, many=True)
    return Response({'wallets': serializer.data},
                    status=HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def wallet_records_lookup(request, waller_ref):
    search_rslt = wallet_search(wallet_ref=waller_ref, return_wallet=True)
    if not search_rslt['status'] == 0:
        return Response({ "message": search_rslt["message"]},status=HTTP_400_BAD_REQUEST)
    else:
        wallet = search_rslt["wallet"]
        wlt_serializer = WalletAllSerializer(wallet)

        records = WalletRecords.objects.filter(wallet_ref=wallet.wallet_ref).order_by("-id")
        records_serializer = WalletRecordsAllSerializer(records, many=True)

        return Response({'wlt_dtls': wlt_serializer.data, 'records_dtls': records_serializer.data},
                status=HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_all_ledgers(request):
    ledgers = Wallet.objects.all().order_by("-id")
    serializer = WalletAllSerializer(ledgers, many=True)
    return Response({'ledgers': serializer.data},
                    status=HTTP_200_OK)
            

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def transaction_view(request):
    transaction_ref = request.data.get('transaction_ref')
    transaction_details = get_transaction_details(transaction_ref)

    transaction = Transactions.objects.get(id=1)
    serializer = TransactionsAllSerializer(transaction)
    part_trans = 0
    return Response({'transaction': serializer.data, "part_trans":part_trans},
                    status=HTTP_200_OK)

