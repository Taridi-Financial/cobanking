import random

from cbsaas.banking.models import LienEntries, Wallet, Wallet, Wallet, Transactions
from cbsaas.cin.services.operations import get_client_cin

def single_transact(
    debit_wallet_ref=None,
    credit_wallet_ref=None,
    amount=None,
    debit_narration=None,
    credit_narration=None,
    **kwargs
):
    transaction = Transactions()
    transaction.transact(
        debit_wallet_ref=debit_wallet_ref,
        credit_wallet_ref=credit_wallet_ref,
        amount=amount,
        debit_narration=debit_narration,
        credit_narration=credit_narration,
        **kwargs
    )
    return {
        "status": 0,
        "message": "Transaction sucessful",
        "transaction_ref": transaction.transaction_ref,
    }

def batch_credit_transact(debit_wallet_ref=None,debit_amount=None,debit_narration=None, overdraw=True, credit_details=None,  **kwargs):
    transaction = Transactions()
    trans_response = transaction.batch_credit(debit_wallet_ref=debit_wallet_ref, debit_narration=debit_narration, debit_amount=debit_amount, overdraw=True, credit_details=credit_details, **kwargs)
    return trans_response

def create_wallet(client_ref=None, wallet_name=None,  wallet_type=None):
    cin_search = get_client_cin(client_ref=client_ref)
    cin = cin_search["cin"]
    if wallet_type == "NORMAL":
        new_wlt = Wallet()
        new_wlt.wallet_ref = random.randint(1000, 10000)
        new_wlt.wallet_name = wallet_name
        new_wlt.status = "pending"
        new_wlt.scheme_code = "NM100"
       
        new_wlt.save()
        new_wlt.cin.add(cin)
        new_wlt.save()
        return {
            "status": 0,
            "message": "Normal Wallet created",
            "wallet_ref": new_wlt.wallet_ref,
        }

    elif wallet_type == "LEDGER":
        new_wlt = Wallet()
        new_wlt.wallet_ref = random.randint(1000, 10000)
        new_wlt.wallet_name = wallet_name
        new_wlt.status = "pending"      
        new_wlt.scheme_code = "LD105"
        new_wlt.save()
        new_wlt.cin.add(cin)
        new_wlt.save()
        return {
            "status": 0,
            "message": "Ledger Wallet created",
            "wallet_ref": new_wlt.wallet_ref,
        }
    elif wallet_type == "LOAN":
        new_wlt = Wallet()
        new_wlt.wallet_ref = random.randint(1000, 10000)
        new_wlt.wallet_name = wallet_name
        new_wlt.status = "active"
        new_wlt.allow_overdraw = True
        new_wlt.scheme_code = "LN100"
        
        new_wlt.save()
        new_wlt.cin.add(cin)
        new_wlt.save()
        return {
            "status": 0,
            "message": "Ledger Wallet created",
            "wallet_ref": new_wlt.wallet_ref,
        }


def generate_wallet_ref(cin=None, wallet_name=None, scheme_code=None, wallet_type=None):
    """To do"""
    pass




def wallet_search(wallet_ref=None, return_wallet=True, select_for_update=False):

    if Wallet.objects.filter(wallet_ref=wallet_ref).exists():
        if return_wallet and select_for_update:
            wallet = Wallet.objects.select_for_update().get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        elif return_wallet:
            wallet = Wallet.objects.get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet_type": "normal","wallet": wallet}
    else:
        return {"status": 1, "message": "Wallet does not exist"}


def get_primary_consumer_wallet(cin=None):
    try:
        wallet = Wallet.objects.filter(cin=cin, scheme_code = "NM100").first()
    except Exception:
        return None
    else:
        return wallet


def get_transaction_details(transaction_ref):
    transaction = Transactions.objects.get(transaction_ref=transaction_ref)



def add_lien(wallet_ref=None, amount=None, narration=None,done_by=None):
    wallet_search = wallet_search(wallet_ref=wallet_ref, return_wallet=True)
    wallet = wallet_search.get("wallet", None)
    if not wallet:
        return {"status": 1, "message": "Wallet does not exist"}
    wallet.add_lien(amount=amount)
    lien_entry =  LienEntries(wallet_ref = wallet_ref, lien_amount = amount,done_by = done_by, narration = narration )
    lien_entry.save()
    return {"status": 0, "lien_entry_id": lien_entry.id}

def release_lien(lien_entry=None, amount=None, done_by=None):
    wallet_search = wallet_search(wallet_ref=lien_entry.wallet_ref, return_wallet=True)
    wallet = wallet_search.get("wallet", None)
    if not wallet:
        return {"status": 1, "message": "Wallet does not exist"}
    """if we have amount it means we are lowering the amoun"""
    if not amount:
        wallet.release_lien(amount=lien_entry.lien_amount)
    if amount > lien_entry.lien_amount:
        return {"status": 1, "message": "Release amount greater than amount held"}
    wallet.release_lien(amount=amount)
    lien_entry.lien_amount = (lien_entry.lien_amount-amount)
    lien_entry.save()