from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from cbsaas.banking.api.serializers import AddLedgerSerializer, LedgerWalletAllSerializer, LedgerWalletRecordsAllSerializer
from cbsaas.banking.models import LedgerWallet, LedgerWalletRecords, Transactions
from cbsaas.banking.services.operations import create_wallet, wallet_search
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
def add_ledger(request):
    serializer = AddLedgerSerializer(data=request.data)
    if serializer.is_valid():
        client_ref=serializer.data['client_ref']
        wallet_name=serializer.data['wallet_name']
        scheme_code=serializer.data['scheme_code']
        wallet_type="LEDGER"
        create_wlt_resp = create_wallet(
            client_ref=client_ref, wallet_name=wallet_name, scheme_code=scheme_code, wallet_type=wallet_type
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


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def view_all_ledgers(request):
    ledgers = LedgerWallet.objects.all().order_by("-id")
    serializer = LedgerWalletAllSerializer(ledgers, many=True)
    return Response({'ledgers': serializer.data},
                    status=HTTP_200_OK)

    


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def wallet_lookup(request, waller_ref):
    search_rslt = wallet_search(wallet_ref=waller_ref, return_wallet=True)
    if search_rslt['status'] == 0:
        if search_rslt["wallet_type"] =="normal":
            wallet = search_rslt["wallet"]
            serializer = LedgerWalletAllSerializer(wallet)
        elif search_rslt["wallet_type"] =="normal":
            wallet = search_rslt["wallet"]
            serializer = LedgerWalletAllSerializer(wallet)
        elif search_rslt["wallet_type"] =="ledger":
            wallet = search_rslt["wallet"]
            wlt_serializer = LedgerWalletAllSerializer(wallet)

            records = LedgerWalletRecords.objects.filter(wallet_ref=wallet.wallet_ref).order_by("-id")
            records_serializer = LedgerWalletRecordsAllSerializer(records, many=True)

            return Response({'wlt_dtls': wlt_serializer.data, 'records_dtls': records_serializer.data},
                    status=HTTP_200_OK)

            
    
    

