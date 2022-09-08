from django.db import models
from django.utils.timezone import now
from cbsaas.banking.models import WalletRecords
from cbsaas.cin.models import CINRegistry
from cbsaas.clients.models import Clients
from cbsaas.ibase.models import GlobalBaseModel

from django.contrib.auth import get_user_model

User = get_user_model()


class Loan(GlobalBaseModel):  
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    cin = models.ManyToManyField(CINRegistry)   #relates to the user who borrowed
    loan_type_code = models.CharField(max_length=100)
    loan_ref = models.CharField(max_length=100)
    applied_amount = models.FloatField(default=0.00)
    amount_disbursed = models.FloatField(default=0.00)
    loan_status = models.CharField(max_length=100)  #preapplication, pending, approved, disbursed, closed 
    applied_by = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=100, blank=True,null=True)
    date_applied = models.CharField(max_length=100)
    date_disbursed = models.DateField(blank=True,null=True)
    date_cleared=models.DateField(blank=True,null=True)
    loan_wallet_ref = models.CharField(max_length=100, blank=True,null=True)
    disbursment_trans_ref = models.CharField(max_length=100, blank=True,null=True)
    disbursment_credit_part_tran = models.CharField(max_length=100, blank=True,null=True) 
    penalty_start = models.DateTimeField(blank=True,null=True)
    penalty_end = models.DateTimeField(blank=True,null=True)
    unrealized_interest = models.FloatField(default=0.00)
    securities_value = models.FloatField(default=0.00)
    securities_coverage = models.CharField(max_length=10, blank=True,null=True) 


class LoanProduct(GlobalBaseModel):  
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)   
    loan_code = models.CharField(max_length=100)
    loan_type = models.CharField(max_length=30, blank=True, null=True) #mobile, business, bosa  add behaviour to the related model 
    description = models.CharField(max_length=100)
    duration = models.CharField(max_length=100) 
    lower_limit = models.FloatField(default=0.00)
    upper_limit = models.FloatField(default=0.00)
    interest_realization = models.CharField(max_length=30, blank=True, null=True) #first, prorated
    loan_period = models.CharField(max_length=30, blank=True, null=True) #in days 
    penalty_period = models.CharField(max_length=20, blank=True, null=True) #in days
    penalty_grace_period = models.CharField(max_length=20, blank=True, null=True) #in days

class LoanProductCharges(GlobalBaseModel):  
    loan_code = models.CharField(max_length=100, blank=True, null=True)
    charge_code = models.CharField(max_length=100, blank=True, null=True)
    charge_frequency = models.CharField(max_length=100, default="oneoff") #One off, daily, weekly, monthly
    charge_moment = models.CharField(max_length=100) #precreation, predisbursment, postdisbursment, interest, ondefault
    charge_value_type = models.CharField(max_length=100) # fixed, percentage
    charge_value = models.CharField(max_length=100) 
    charge_destination = models.CharField(max_length=100, null=True) 

    def calculate_charge(self, amount=None):
        if self.charge_value_type == "fixed":
            return self.charge_value
        else:
            return float(amount) * float(self.charge_value)

class LoanAmotization(GlobalBaseModel):  
    loan_ref =  models.CharField(max_length=100) 
    due_date = models.CharField(max_length=100)
    amount_due= models.FloatField(default=0.00)
    amount_paid = models.FloatField(default=0.00)
    payment_status = models.CharField(max_length=100)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(blank=True, null=True)


class LoanAmotizationPayments(GlobalBaseModel):  
    wallet_record = models.OneToOneField(WalletRecords, on_delete=models.CASCADE)
    loan_amotization_entry = models.ForeignKey(LoanAmotization, on_delete=models.CASCADE)
    amount =  models.FloatField(default=0.00)


class LoanSecurities(GlobalBaseModel):  
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    security_type = models.CharField(max_length=100) #cash, lien, asset
    value = models.FloatField(default=0.00)
    narration = models.CharField(max_length=100, blank=True, null=True) #First charge on the asset. 
    security_id = models.CharField(max_length=100, blank=True, null=True)


# class MobileLoanProductCharges(LoanProductCharges):  
#     mobile_loan_product = models.ForeignKey(MobileLoanProduct, on_delete=models.CASCADE)
#     class Meta:
#         abstract = True

# class LoansActions(GlobalBaseModel):  
#     loan_ref =  models.CharField(max_length=100, blank=True, null=True) 
#     action_by = models.CharField(max_length=100, blank=True, null=True)
#     narration = models.CharField(max_length=100, blank=True, null=True)
#     action_value = models.CharField(max_length=100, blank=True, null=True) 
#    
    

#     class Meta:
#         abstract = True

# class MobileLoanActions(LoansActions):   
#     pass


# def disurse(loan=None,debit_amount=None, credit_details=None):
#     pass

# # class LoansLimits(GlobalBaseModel):  
# #     cin = models.ForeignKey(CINRegistry, on_delete=models.CASCADE, blank=True, null=True) 