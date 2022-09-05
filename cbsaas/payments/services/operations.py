
"""To manage all the operations around transactions . The god model, the doer of all """
import uuid
import requests
from cbsaas.payments.models import PaymentsTransactionMonitor, WalletPaymentsDetails, WalletPaymentsRecords

def record_payments_transaction_monitor(wallet, amount, trans_ref,wallet_record_id, **kwargs):
    # if wallet.scheme_code == "LD105":
    if wallet.wallet_ref == '6567':
        initiate_payment = kwargs.get('wallet_record_id', True)
        payment_dest = kwargs.get('payment_dest', True)
        if not PaymentsTransactionMonitor.objects.filter(wallet_record_id=wallet_record_id).exists():
            transaction_monitor = PaymentsTransactionMonitor()
            transaction_monitor.wallet_record_id = wallet_record_id
            transaction_monitor.amount = amount
            transaction_monitor.wallet_ref = wallet.wallet_ref
            transaction_monitor.initiate_payment = initiate_payment
            transaction_monitor.payment_dest = payment_dest
            transaction_monitor.payment_status = ""
            if initiate_payment is False:
                transaction_monitor.initiate_payment = False
            transaction_monitor.save()
            payment_operator = PaymentsMonitorOperations(transaction_monitor=transaction_monitor)
            payment_operator.action_request()


# def payments_payment_out(wallet_ref=None, amount=None,wallet_record_id=None ):
#     provider=get_wallet_payments_provider(wallet_ref=wallet_ref)
#     if provider == "MPESA":
#         pass
#     elif provider == "AIRTEL_M":
#         pass
#     elif provider == "EQUITY":
#         pass

# def get_wallet_payments_provider(wallet_ref=None):
#     pass

# def payments_collect_funds():
#     pass

# def payments_check_trans_status():
#     pass

class PaymentsMonitorOperations():
    def __init__(self, transaction_monitor=None, action_by="system", **kwargs) -> None:
        self.transaction_monitor = transaction_monitor
        self.action_by =  action_by
        self.operation_status = None
        self.operation_message = None
        self.request_dest= None
        self.request_payload = None
        

    def set_request_record(self):
        self.wallet_payments_record = WalletPaymentsRecords()
        self.wallet_payments_record.transaction_monitor = self.transaction_monitor
        self.wallet_payments_record.request_id = uuid.uuid4().hex
        self.wallet_payments_record.save()

    def format_payment_request(self):
        payment_provider_details = WalletPaymentsDetails.objects.filter(wallet_ref=self.transaction_monitor.wallet_ref).first()
        if not payment_provider_details:
            pass
        else:
            request_dest = payment_provider_details.provider_url
            request_payload = {}
            request_payload["client_ref"]= "http" 
            request_payload["provider"]= payment_provider_details.provider
            request_payload["wallet_ref"]= self.transaction_monitor.wallet_ref
            request_payload["amount"]=  self.transaction_monitor.amount
            request_payload["payment_dest"]= self.transaction_monitor.payment_dest
            request_payload["request_id"]= self.wallet_payments_record.request_id
            
            self.request_dest = request_dest
            self.request_payload = request_payload

    def send_payment_request(self):
        requests.post(self.request_dest, data=self.request_payload)
    
    def action_request(self):
        self.set_request_record()
        self.format_payment_request()
        self.send_payment_request()

class PaymentCollectionsOperations():
    def __init__(self, wallet=None,trans_ref=None,wallet_record_id=None, amount=None, phone_number=None, action_by="wen", **kwargs) -> None:
        self.amount = float(amount)