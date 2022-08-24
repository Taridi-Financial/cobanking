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
    loan_status = models.CharField(max_length=100)  #preapplication, pending, 
    applied_by = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=100, blank=True,null=True)
    date_applied = models.CharField(max_length=100)
    date_disbursed = models.DateField(blank=True,null=True)
    date_cleared=models.DateField(blank=True,null=True)
    loan_wallet_ref = models.CharField(max_length=100, blank=True,null=True)
    disbursment_trans_ref = models.CharField(max_length=100, blank=True,null=True)
    dsbsment_credit_part_tran = models.CharField(max_length=100, blank=True,null=True) 

    class Meta:
        abstract = True

class MobileLoans(Loan):  
    pass


class LoanProduct(GlobalBaseModel):  
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)   
    loan_code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    duration = models.CharField(max_length=100) 
    lower_limit = models.CharField(max_length=100, default=0)
    upper_limit = models.CharField(max_length=100)

    class Meta:
        abstract = True

class MobileLoanProduct(LoanProduct):  
    pass

class LoanProductCharges(GlobalBaseModel):  
    loan_code = models.CharField(max_length=100, blank=True, null=True)
    charge_code = models.CharField(max_length=100, blank=True, null=True)
    charge_frequency = models.CharField(max_length=100, default="oneoff") #One off, recurring
    charge_moment = models.CharField(max_length=100) #precreation, predisbursment, postdisbursment, oninterest, ondefault
    charge_value_type = models.CharField(max_length=100) # fixed, percentage
    charge_value = models.CharField(max_length=100) 
    charge_destination = models.CharField(max_length=100, null=True) 

    class Meta:
        abstract = True 

    def calculate_charge(self, amount=None):
        if self.charge_value_type == "fixed":
            return self.charge_value
        else:
            return float(amount) * float(self.charge_value)

    def add_lien(self, amount=None):
        return 500

class MobileLoanProductCharges(LoanProductCharges):  
    mobile_loan_product = models.ForeignKey(MobileLoanProduct, on_delete=models.CASCADE)

class LoansActions(GlobalBaseModel):  
    loan_ref =  models.CharField(max_length=100, blank=True, null=True) 
    action_code = models.CharField(max_length=100, blank=True, null=True)
    narration = models.CharField(max_length=100, blank=True, null=True)
    action_value = models.CharField(max_length=100, blank=True, null=True) 
    

    class Meta:
        abstract = True

class MobileLoanActions(LoansActions):   
    pass


def disurse(loan=None,debit_amount=None, credit_details=None):
    pass


