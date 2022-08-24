from random import choice
from string import ascii_uppercase
from rest_framework import serializers
from django.db import models
from cbsaas.banking.services.operations import batch_credit_transact, create_wallet, single_transact
from cbsaas.ibase.models import GlobalBaseModel
from cbsaas.lending.models import MobileLoanProductCharges, MobileLoans
from cbsaas.parameters.services.operations import get_wallet_ref_from_code



class MobileLoansOperations(models.Model):   
    def __init__(self, loan_ref=None, client_ref=None, amount=None, loan_code=None,phone_number=None, action_by="wen") -> None:
        self.loan_ref = loan_ref
        self.amount = float(amount)
        self.phone_number =  phone_number
        self.client_ref = client_ref
        self.loan_code = loan_code
        self.action_by =  action_by

        self.operation_status = None

    def set_loan(self):
        """FOR PROCESSING EXISTING LOANS"""
        loan = MobileLoans.objects.get(loan_ref=self.loan_ref)
        self.loan = loan


    def apply_loan(self, disburse_wallet=None):
        self.process_preapplication()
        if not self.operation_status == 0:
            self.set_application_to_pending()
        if not self.operation_status == 0:
            self. approve_loan()
        if not self.operation_status == 0:
            self.create_loan_wallet()
        if not self.operation_status == 0:
            self.disburse_loan(disburse_wallet=disburse_wallet)
       
        return self.loan_ref

    def process_preapplication(self):
        new_loan = MobileLoans()
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

    def approve_loan(self, action_by="wen"):
        self.set_loan()
        self.loan.approved_by = action_by
        self.loan.loan_status = "approved"
        self.loan.save()
        

    def disburse_loan(self, disburse_wallet=None):
        self.set_loan()
        self.charge_details = calculate_charges(loan_code=self.loan_code, amount=self.amount)
        # get the predisbursement charges 
        credit_details = []
        self.disburse_amount = self.amount
        # process pre disbursment charges
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
            return batch_process
        else:
            return batch_process

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
        return trans_dtls


def get_disbursment_values(loan_code=None, amount=None):
    charges = MobileLoanProductCharges.objects.filter(loan_code=loan_code)
    return {"disburse_amount": 1000, "interest": 100,  "loan_amount":1100, "loan_balance":1100 , "principle":1000}


def calculate_charges(loan_code=None, amount=None):
    charges = MobileLoanProductCharges.objects.filter(loan_code=loan_code)
    charge_details = []
    for charge in charges:
        
        amount_to_charge = charge.add_lien(amount=amount)
        
        serializer = CalculateChargeSerializer(charge)
        serializer_details = serializer.data
        serializer_details["amount_to_charge"] = 500
        charge_details.append(serializer_details)
        
    return charge_details

class CalculateChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileLoanProductCharges
        fields = ('__all__')

"""TO DO 
Charge processing>
Add the specified charges
Monitor the charge times
Monitor the charge amounts 
Give the charge and the destination accounts 
"""




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