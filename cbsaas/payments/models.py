from django.db import models
from cbsaas.banking.models import WalletRecords

from cbsaas.ibase.models import GlobalBaseModel


class WalletPaymentsDetails(GlobalBaseModel):
    wallet_ref = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    provider_url = models.CharField(max_length=100)


class PaymentsTransactionMonitor(GlobalBaseModel):
    wallet_record = models.OneToOneField(WalletRecords, on_delete=models.CASCADE)
    wallet_ref = models.CharField(max_length=100)
    initiate_payment = models.BooleanField(default=True)
    payment_inintiated = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=100)
    amount = models.FloatField(default=0.00)
    payment_dest = models.CharField(max_length=300)
    provider_transaction_code = models.CharField(max_length=100, blank=True, null=True)


class WalletPaymentsRecords(GlobalBaseModel):
    """Request details"""
    transaction_monitor = models.ForeignKey(PaymentsTransactionMonitor, on_delete=models.CASCADE)
    request_id = models.CharField(max_length=300)
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    """Result details """
    result_payload = models.CharField(max_length=1000, blank=True, null=True)
    result_timestamp = models.DateTimeField(blank=True, null=True)
    result_status = models.CharField(max_length=300, blank=True, null=True) #success, failed  
    provider_transaction_code = models.CharField(max_length=300, blank=True, null=True) #success, failed 

    # """Response details"""
    # response_payload = models.CharField(max_length=1000, blank=True, null=True)
    # response_timestamp = models.DateTimeField(blank=True, null=True)
    # response_id = models.CharField(max_length=300, blank=True, null=True)
    # respone_status = models.CharField(max_length=300, blank=True, null=True) #success, failed    
    


class MoneyCollections(models.Model):
    client = models.CharField(max_length=300, blank=True, null=True)
    amount = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=300, blank=True, null=True)
    internal_ref = models.CharField(max_length=300, blank=True, null=True)
    trans_type = models.CharField(max_length=300, blank=True, null=True)
    trans_code = models.CharField(max_length=300, blank=True, null=True)
    money_provider_ref  = models.CharField(max_length=300, blank=True, null=True)
    initial_response_payload = models.CharField(max_length=1000, blank=True, null=True)
    callback_payload = models.CharField(max_length=1000, blank=True, null=True)  
    status = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    callback_timestamp = models.DateTimeField(blank=True, null=True)


class WalletCollectionsRecords(GlobalBaseModel):
    """Request details"""
    transaction_monitor = models.ForeignKey(PaymentsTransactionMonitor, on_delete=models.CASCADE)
    request_id = models.CharField(max_length=300)