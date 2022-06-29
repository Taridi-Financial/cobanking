from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from cbsaas.banking.api.serializers import CreateLedgerWalletSerializer
from cbsaas.banking.models import Transactions
from cbsaas.banking.services.operations import create_wallet
from cbsaas.clients.models import Clients


@api_view(["POST"])
def holder(request):
    pass


@api_view(["POST"])
def move_funds(request):
    transaction = Transactions()
    transaction.transact(debit_wallet_ref=0, credit_wallet_ref=0, amount=0)


@api_view(["POST"])
def deposit_funds(request):
    transaction = Transactions()
    transaction.transact(debit_wallet_ref=0, credit_wallet_ref=0, amount=0)


@api_view(["POST"])
def add_ledger(request):
    serializer = CreateLedgerWalletSerializer(request.data)
    if serializer.is_valid():
        client = Clients.objects.all().first()
        create_wlt_resp = create_wallet(
            cin=client.cin, wallet_name=None, scheme_code=None, wallet_type=None
        )
        action_status = create_wlt_resp["status"]
        message = create_wlt_resp["message"]
        if action_status == 1:
            return Response(
                {"status": action_status, "message": message},
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"status": action_status, "message": message}, status=HTTP_200_OK
            )

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
