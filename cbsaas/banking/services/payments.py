from cbsaas.banking.models import PaymentsTransactionMonitor

def record_payments_transaction_monitor(wallet, amount, trans_ref,wallet_record_id, **kwargs):
    if wallet.scheme_code == "LD105":
        initiate_payment = kwargs.get('wallet_record_id', None)
        transaction_monitor = PaymentsTransactionMonitor(wallet_ref=wallet.wallet_ref, 
                                                        wallet_record_id =wallet_record_id
                                                        )
        if initiate_payment and initiate_payment is False:
            transaction_monitor.initiate_payment = False
            transaction_monitor.payment_status = ""
        transaction_monitor.payment_status = ""
        transaction_monitor.save()



def payments_payment_out(wallet_ref=None, amount=None,wallet_record_id=None ):
    provider=get_wallet_payments_provider(wallet_ref=wallet_ref)
    if provider == "MPESA":
        pass
    elif provider == "AIRTEL_M":
        pass
    elif provider == "EQUITY":
        pass

def get_wallet_payments_provider(wallet_ref=None):
    pass

def payments_collect_funds():
    pass

def payments_check_trans_status():
    pass