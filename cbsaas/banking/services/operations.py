import random

from cbsaas.banking.models import LedgerWallet, LoanWallet, NormalWallet, Transactions


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


def create_wallet(
    client_ref=None, wallet_name=None, scheme_code=None, wallet_type=None
):
    cin = None
    if wallet_type == "normal":
        new_wlt = NormalWallet()
        new_wlt.wallet_ref = random.randint(1000, 10000)
        new_wlt.wallet_name = wallet_name
        new_wlt.status = "pending"
        new_wlt.scheme_code = scheme_code
        new_wlt.cin = cin
        new_wlt.save()
        return {
            "status": 0,
            "message": "Normal Wallet created",
            "wallet_ref": new_wlt.wallet_ref,
        }

    elif wallet_type == "ledger":
        new_wlt = LedgerWallet()
        new_wlt.wallet_ref = random.randint(1000, 10000)
        new_wlt.wallet_name = wallet_name
        new_wlt.status = "pending"
        new_wlt.scheme_code = scheme_code
        new_wlt.save()
        return {
            "status": 0,
            "message": "Ledger Wallet created",
            "transaction_ref": new_wlt.wallet_ref,
        }
    elif wallet_type == "loan":
        new_wlt = LoanWallet()
        new_wlt.wallet_ref = random.randint(1000, 10000)
        new_wlt.wallet_name = wallet_name
        new_wlt.status = "pending"
        new_wlt.scheme_code = scheme_code
        new_wlt.save()
        return {
            "status": 0,
            "message": "Ledger Wallet created",
            "transaction_ref": new_wlt.wallet_ref,
        }


def generate_wallet_ref(cin=None, wallet_name=None, scheme_code=None, wallet_type=None):
    """To do"""
    pass
