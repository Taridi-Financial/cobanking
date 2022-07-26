from random import choice
from string import ascii_uppercase
from django.db import models
from cbsaas.banking.services.operations import batch_credit_transact, create_wallet, single_transact
from cbsaas.ibase.models import GlobalBaseModel
from cbsaas.lending.models import MobileLoans
from cbsaas.parameters.services.operations import get_wallet_ref_from_code



class MobileLoansOperations(models.Model):   
    def __init__(self, loan_ref=None) -> None:
        self.loan_ref = loan_ref

    def set_loan(self):
        loan = MobileLoans.objects.get(loan_ref=self.loan_ref)
        self.loan = loan


    def apply_loan(self, client_ref=None, amount=None, loan_code=None,phone_number=None):
        """To Do """
        new_loan = MobileLoans()
        new_loan.loan_type_code = loan_code
        loan_ref = ''.join(choice(ascii_uppercase)for i in range(15))
        new_loan.loan_ref = loan_ref
        new_loan.applied_amount = amount
        new_loan.loan_status = "pending"
        new_loan.applied_by = "wen"
        new_loan.client_ref = client_ref
        new_loan.save()
        self.loan_ref = loan_ref
        return new_loan.loan_ref

    def disburse_loan(self):
        self.set_loan()
        disbursments_wlt_dtls = get_wallet_ref_from_code(client_ref=self.loan.client_ref, use_type_code="SMSCHARGE", branch_code=None)
        interest_wlt_dtls = get_wallet_ref_from_code(client_ref=self.loan.client_ref, use_type_code="LNINCOME", branch_code=None)
        admn_fee_wlt_dtls = get_wallet_ref_from_code(client_ref=self.loan.client_ref, use_type_code="LNFEEINCOME", branch_code=None)
        loan_wlt_dtls = create_wallet(client_ref=self.loan.client_ref, wallet_name="wen", scheme_code="LW100", wallet_type="loan")
        credit_details = [
            {"wallet_ref":disbursments_wlt_dtls["wallet_ref"], "amount":2400},
            {"wallet_ref":interest_wlt_dtls["wallet_ref"], "amount":200},
            {"wallet_ref":admn_fee_wlt_dtls["wallet_ref"], "amount":450}
        ]
        loan_wallet_ref = loan_wlt_dtls["wallet_ref"]
        self.loan.loan_wallet_ref = loan_wallet_ref
        self.loan.save()
        batch_process = batch_credit_transact(debit_wallet_ref= loan_wallet_ref,debit_amount=3050,debit_narration="Dibursment of loan",overdraw=True, credit_details=credit_details)
        return batch_process

    def repay_loan(self, source_wlt =None, amount=None):
        self.set_loan()
        self.loan.save()
        narration = f"Repayment of loan {self.loan.loan_ref}"
        trans_dtls = single_transact(debit_wallet_ref=source_wlt,credit_wallet_ref=self.loan.loan_wallet_ref,amount=amount,debit_narration=narration,credit_narration=narration)
        return trans_dtls


def get_disbursment_values(loan_code=None, amount=None):
    
    return {"disburse_amount": 1000, "interest": 100,  "loan_amount":1100, "loan_balance":1100 , "principle":1000}


"""TO DO 
Charge processing>
Add the specified charges
Monitor the charge times
Monitor the charge amounts 
Give the charge and the destination accounts 
"""