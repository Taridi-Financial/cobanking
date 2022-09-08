from array import array
from random import choice
from string import ascii_uppercase
from cbsaas.banking.models import wallet_search
from rest_framework import serializers
from django.db import models
from cbsaas.banking.services.operations import batch_credit_transact, create_wallet, single_transact
from cbsaas.ibase.models import GlobalBaseModel
from cbsaas.lending.models import LoanProductCharges, Loan
from cbsaas.parameters.services.operations import get_wallet_ref_from_code



class LoanOperations(models.Model):   
    def __init__(self,**kwargs) -> None:
        self.__dict__.update(kwargs)
        self.operation_status = 0
        self.operation_msg = None
        """Arguments list
        To apply :
        client_ref=None, amount=None, loan_code=None,phone_number=None,applicant_cin=None, action_by=None, loan_type = standard/mobile
        To aprove update or other actions
        loan_ref=None
        """        

    def set_loan(self):
        """FOR PROCESSING EXISTING LOANS"""
        loan = Loan.objects.get(loan_ref=self.loan_ref)
        self.loan = loan

    def set_loan_wallet(self):
        """used by methods that manipulate the wallet like zerorize, repay
           Requires loan to be set 
        """
        self.loan_wallet = wallet_search(wallet_ref=self.loan.loan_wallet_ref, return_wallet=True)
        


    def apply_loan(self, disburse_wallet=None) -> str:
        """0 proceed any other status fail"""
        self.process_preapplication()
        if not self.operation_status > 0:
            self.set_application_to_pending()
        if not self.operation_status > 0:
            self.approve()
        if not self.operation_status > 0:
            self.create_loan_wallet()
        if not self.operation_status > 0:
            self.disburse_loan(disburse_wallet=disburse_wallet)
       
        return self.operation_msg

    def process_preapplication(self):
        new_loan = Loan()
        new_loan.loan_type_code = self.loan_code
        loan_ref = ''.join(choice(ascii_uppercase)for i in range(15))
        new_loan.loan_ref = loan_ref
        new_loan.applied_amount = self.amount
        new_loan.loan_status = "preapplication"
        new_loan.applied_by = self.action_by
        new_loan.client_ref = self.client_ref
        new_loan.save()
        self.loan_ref = loan_ref

    def set_application_to_pending(self):
        self.set_loan()
        self.loan.loan_status = "pending"
        self.loan.save()
        if check_autoapproval(loan_code=self.loan_code,applicant_cin=self.applicant_cin, amount=self.amount) is False:
            self.operation_status = 1
            self.operation_msg = f"Loan application pending loan ref: {self.loan_ref}"

    def approve(self,action_type=None, action_by="wen"):
        self.set_loan()
        if action_type== "approve":
            self.loan.approved_by = action_by
            self.loan.loan_status = "approved"
            self.loan.save()
            self.operation_msg = f"Loan application approved pending disbursment loan ref: {self.loan_ref}"
        else:
            self.loan.approved_by = action_by
            self.loan.loan_status = "rejected"
            self.loan.save()
            self.operation_msg = f"Loan application rejected loan ref:: {self.loan_ref}"
        

    def disburse_loan(self, disburse_wallet=None):
        self.set_loan()
        self.charge_details = calculate_charges(loan_code=self.loan_code, amount=self.amount)
        """Get the predisbursement charges """
        credit_details = []
        self.disburse_amount = self.amount
        """Process pre disbursment charges"""
        for charge in self.charge_details:
            if charge["charge_moment"] == "predisbursment":
                self.disburse_amount = float(self.disburse_amount) - float(charge["amount_to_charge"])           
                # wlt_details = get_wallet_ref_from_code(client_ref=self.loan.client_ref, use_type_code=charge["charge_destination"], branch_code=None) 
                single_charge_dtls = {}
                single_charge_dtls["wallet_ref"] = charge["charge_destination"]
                single_charge_dtls["amount"] = charge["amount_to_charge"]
                credit_details.append(single_charge_dtls)

        # process disbursement details, weather it is disbursed through cash, mpesa, airtel money
        disbursement_dtls = {} 
        disbursement_dtls["wallet_ref"] = disburse_wallet
        disbursement_dtls["amount"] = self.disburse_amount
        credit_details.append(disbursement_dtls)

        batch_process = batch_credit_transact(debit_wallet_ref= self.loan.loan_wallet_ref,debit_amount=self.amount,debit_narration="Dibursment of loan",overdraw=True, credit_details=credit_details)
        if batch_process["status"] == 0:
            self.loan.loan_status = "disbursed"
            self.loan.save()
            trans_ref = batch_process["trans_ref"]
            self.operation_msg = f"Loan disbursment successful, funds credited with transaction ref: {trans_ref} loan ref: {self.loan_ref}" 
            return self.operation_msg
        else:
            batch_msg = batch_process["message"]
            self.operation_msg = f"Loan disbursment failed reason reason: {batch_msg}" 
            return self.operation_msg

    def create_loan_wallet(self):        
        loan_wlt_dtls = create_wallet(client_ref=self.loan.client_ref, wallet_name="wen", wallet_type="LOAN")
        loan_wallet_ref = loan_wlt_dtls["wallet_ref"]
        self.loan.loan_wallet_ref = loan_wallet_ref
        self.loan.save()

    def repay_loan(self, source_wlt =None, amount=None):
        self.set_loan()
        self.loan.save()
        narration = f"Repayment of loan {self.loan.loan_ref}"
        trans_dtls = single_transact(debit_wallet_ref=source_wlt,credit_wallet_ref=self.loan.loan_wallet_ref,amount=amount,debit_narration=narration,credit_narration=narration)
        if trans_dtls["status"] == 0:
            trans_ref = trans_dtls["trans_ref"]
            self.operation_msg = f"Loan repayment successful, funds credited with transaction ref: {trans_ref} loan ref: {self.loan_ref}" 
            return self.operation_msg
        return trans_dtls

    def close_loan(self):
        self.set_loan()
        self.set_loan_wallet()
        loan_wallet_balance = self.loan_wallet.balance
        
        if loan_wallet_balance < 0:
            self.operation_msg = f"Loan not yet paid off, kindly pay off the loan before closing the loan" 
            return self.operation_msg
        if loan_wallet_balance > 0:
            self.operation_msg = f"Loan not yet zerorized, Zerorize the loan wallet before clearing the loan" 
            return self.operation_msg
        self.loan.loan_status = "closed"
        self.loan.save()
        self.loan_wallet.status = 'closed'
        self.loan_wallet.save()
        self.operation_msg = f"Loan closed successfully" 
        return self.operation_msg

    def zerorize_loan(self, destination_wlt=None):
        """Called if the loan account balance is > 0, meaning there is an overpayment"""
        self.set_loan()
        self.set_loan_wallet()
        # loan_wallet = wallet_search(wallet_ref=self.loan.loan_wallet_ref, return_wallet=True)
        narration = f"Zerorization of the loan wallet {self.loan_wallet.wallet_ref} for loan {self.loan_ref}"
        trans_dtls = single_transact(debit_wallet_ref=self.loan_wallet.wallet_ref,credit_wallet_ref=destination_wlt,amount=self.loan_wallet.balance,debit_narration=narration,credit_narration=narration)
        status = trans_dtls["status"]
        if not status == 0:
            self.operation_msg = f"Zerorization of loan {self.loan_ref} failed, reason {self.loan_ref}" 
            return self.operation_msg
        trans_ref = trans_dtls["trans_ref"]
        self.operation_msg = f"Zerorization of loan successful, funds credited with transaction ref: {trans_ref} loan ref: {self.loan_ref}" 
        return self.operation_msg

    
    def process_post_wallet_credit(self):
        self.set_loan()
        self.set_loan_wallet()
        loan_wallet = wallet_search(wallet_ref=self.loan.loan_wallet_ref, return_wallet=True)

    def add_loan_security(self) -> None:
        pass

    
def get_disbursment_values(loan_code=None, amount=None):
    charges = LoanProductCharges.objects.filter(loan_code=loan_code)
    return {"disburse_amount": 1000, "interest": 100,  "loan_amount":1100, "loan_balance":1100 , "principle":1000}

def check_autoapproval(loan_code=None, applicant_cin=None, amount=None):
    return False


def calculate_charges(loan_code=None, amount=None) -> array:
    charges = LoanProductCharges.objects.filter(loan_code=loan_code)
    charge_details = []
    for charge in charges:        
        serializer = CalculateChargeSerializer(charge)
        serializer_details = serializer.data
        serializer_details["amount_to_charge"] = charge.calculate_charge( amount=amount)
        charge_details.append(serializer_details)
        
    return charge_details

class CalculateChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProductCharges
        fields = ('__all__')

"""TO DO 
Charge processing>
Add the specified charges
Monitor the charge times
Monitor the charge amounts 
Give the charge and the destination accounts 
"""


def update_amotization_table(loan_code=None, amount=None):
    charges = LoanProductCharges.objects.filter(loan_code=loan_code)



# import pandas as pd
# from datetime import date
# import numpy as np
# from collections import OrderedDict
# from dateutil.relativedelta import *


# def amortize(principal, interest_rate, years, addl_principal=0, annual_payments=12, start_date=date.today()):

#     pmt = -round(np.pmt(interest_rate/annual_payments, years*annual_payments, principal), 2)
#     # initialize the variables to keep track of the periods and running balances
#     p = 1
#     beg_balance = principal
#     end_balance = principal

#     while end_balance > 0:

#         # Recalculate the interest based on the current balance
#         interest = round(((interest_rate/annual_payments) * beg_balance), 2)

#         # Determine payment based on whether or not this period will pay off the loan
#         pmt = min(pmt, beg_balance + interest)
#         principal = pmt - interest

#         # Ensure additional payment gets adjusted if the loan is being paid off
#         addl_principal = min(addl_principal, beg_balance - principal)
#         end_balance = beg_balance - (principal + addl_principal)

#         yield OrderedDict([('Month',start_date),
#                            ('Period', p),
#                            ('Begin Balance', beg_balance),
#                            ('Payment', pmt),
#                            ('Principal', principal),
#                            ('Interest', interest),
#                            ('Additional_Payment', addl_principal),
#                            ('End Balance', end_balance)])

#         # Increment the counter, balance and date
#         p += 1
#         start_date += relativedelta(months=1)
#         beg_balance = end_balance