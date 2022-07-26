from django.db import models
from django.utils.timezone import now
from cbsaas.clients.models import Clients
from cbsaas.ibase.models import GlobalBaseModel

from django.contrib.auth import get_user_model

User = get_user_model()



class Loan(GlobalBaseModel):  
    client_ref = models.CharField(max_length=300, blank=True, null=True)
    loan_type_code = models.CharField(max_length=100)
    loan_ref = models.CharField(max_length=100, blank=True,null=True)
    applied_amount = models.CharField(max_length=100)
    amount_disbursed = models.CharField(max_length=100, default=0)
    loan_status = models.CharField(max_length=100)
    applied_by = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=100, blank=True,null=True)
    date_applied = models.CharField(max_length=100)
    date_disbursed = models.DateField(blank=True,null=True)
    date_cleared=models.DateField(blank=True,null=True)
    loan_wallet_ref = models.CharField(max_length=100, blank=True,null=True)


    class Meta:
        abstract = True



class MobileLoans(Loan):  
    pass


class LoanProduct(GlobalBaseModel):  
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)   
    loan_code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    duration = models.CharField(max_length=100) 
    lower_limit = models.CharField(max_length=100)
    upper_limit = models.CharField(max_length=100)

    def get_disbursment_values(self, applied_amount=None):
        charge = LoanProductCharges.objects.get(id=1)
        return {"disburse_amount": 1000, "interest": 100,  "loan_amount":1100, "loan_balance":1100 , "principle":1000}

class LoanProductCharges(GlobalBaseModel):  
    charge_frequency = models.CharField(max_length=100) #One off, recurring
    charge_moment = models.CharField(max_length=100) #before creation, before disbursment, during disbursment, after disbursment
    charge_value_type = models.CharField(max_length=100) # fixed, percentage
    charge_value = models.CharField(max_length=100) 
    charge_destination = models.CharField(max_length=100, blank=True, null=True) 
    


# class MobileLoansActions(GlobalBaseModel):   
#     pass


def disurse(loan=None,debit_amount=None, credit_details=None):
    pass


