from django.db import models

from cbsaas.ibase.models import GlobalBaseModel


class WalletPaymentsRecords(GlobalBaseModel):
    """Request details"""
    amount = models.CharField(max_length=300)
    payment_dest = models.CharField(max_length=300)
    internal_request_id = models.CharField(max_length=300)
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    """Response details"""
    response_payload = models.CharField(max_length=1000, blank=True, null=True)
    response_timestamp = models.DateTimeField(blank=True, null=True)
    response_id = models.CharField(max_length=300, blank=True, null=True)
    respone_status = models.CharField(max_length=300, blank=True, null=True) #success, failed    
    """Result details """
    result_payload = models.CharField(max_length=1000, blank=True, null=True)
    result_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class MpesaPaymentsRecords(WalletPaymentsRecords):
    pass

"""To be implemented """
# class AirtelMoneyPaymentsRecords(WalletPaymentsRecords):
#     pass

# class UnBoundWalletPaymentsRecords(GlobalBaseModel):
#     """Records received when there is no initiation of a transaction"""
#     result_payload = models.CharField(max_length=1000, blank=True, null=True)
#     result_timestamp = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         abstract = True
