import random

from cbsaas.banking.models import LedgerWallet, LoanWallet, NormalWallet, Transactions
from cbsaas.cin.services.operations import get_client_cin


def get_transaction_details(transaction_ref):
    """To do"""
    pass


def single_transact(
    debit_wallet_ref=None,
    credit_wallet_ref=None,
    amount=None,
    debit_narration=None,
    credit_narration=None,
):
    transaction = Transactions()
    transaction.transact(
        debit_wallet_ref=debit_wallet_ref,
        credit_wallet_ref=credit_wallet_ref,
        amount=amount,
        debit_narration=debit_narration,
        credit_narration=credit_narration,
    )
    return {
        "status": 0,
        "message": "Transaction sucessful",
        "transaction_ref": transaction.transaction_ref,
    }

def batch_credit_transact(debit_wallet_ref=None,debit_amount=None,debit_narration=None, overdraw=True, credit_details=None):
    transaction = Transactions()
    trans_response = transaction.batch_credit(debit_wallet_ref=debit_wallet_ref, debit_narration=debit_narration, debit_amount=debit_amount, overdraw=True, credit_details=credit_details)
    return trans_response

def create_wallet(client_ref=None, wallet_name=None, scheme_code=None, wallet_type=None):
    cin_search = get_client_cin(client_ref=client_ref)
    cin = cin_search["cin"]
    if wallet_type == "normal":
        new_wlt = NormalWallet()
        new_wlt.wallet_ref = random.randint(1000, 10000)
        new_wlt.wallet_name = wallet_name
        new_wlt.status = "pending"
        new_wlt.scheme_code = scheme_code
       
        new_wlt.save()
        new_wlt.cin.add(cin)
        return {
            "status": 0,
            "message": "Normal Wallet created",
            "wallet_ref": new_wlt.wallet_ref,
        }

    elif wallet_type == "LEDGER":
        new_wlt = LedgerWallet()
        new_wlt.wallet_ref = random.randint(1000, 10000)
        new_wlt.wallet_name = wallet_name
        new_wlt.status = "pending"
        new_wlt.cin = cin
        
        new_wlt.scheme_code = scheme_code
        new_wlt.save()
        
        return {
            "status": 0,
            "message": "Ledger Wallet created",
            "wallet_ref": new_wlt.wallet_ref,
        }
    elif wallet_type == "loan":
        new_wlt = LoanWallet()
        new_wlt.wallet_ref = random.randint(1000, 10000)
        new_wlt.wallet_name = wallet_name
        new_wlt.status = "active"
        new_wlt.allow_overdraw = True
        new_wlt.scheme_code = scheme_code
        
        new_wlt.save()
        new_wlt.cin.add(cin)
        return {
            "status": 0,
            "message": "Ledger Wallet created",
            "wallet_ref": new_wlt.wallet_ref,
        }


def generate_wallet_ref(cin=None, wallet_name=None, scheme_code=None, wallet_type=None):
    """To do"""
    pass




def wallet_search(wallet_ref=None, return_wallet=True, select_for_update=False):

    if NormalWallet.objects.filter(wallet_ref=wallet_ref).exists():
        if return_wallet and select_for_update:
            wallet = NormalWallet.objects.select_for_update().get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        elif return_wallet:
            wallet = NormalWallet.objects.get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet_type": "normal","wallet": wallet}

    elif LoanWallet.objects.filter(wallet_ref=wallet_ref).exists():
        if return_wallet and select_for_update:
            wallet = LoanWallet.objects.select_for_update().get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        elif return_wallet:
            wallet = LoanWallet.objects.get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet_type": "loan","wallet": wallet}

    elif LedgerWallet.objects.filter(wallet_ref=wallet_ref).exists():
        if return_wallet and select_for_update:
            wallet = LedgerWallet.objects.select_for_update().get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        elif return_wallet:
            wallet = LedgerWallet.objects.get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet_type": "ledger", "wallet": wallet}
    else:
        return {"status": 1, "message": "Wallet does not exist"}



