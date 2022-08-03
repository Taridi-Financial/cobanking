from random import choice
from string import ascii_uppercase

from django.db import models, transaction
from cbsaas.cin.models import CINRegistry
from cbsaas.ibase.models import GlobalBaseModel
from . import signals


class Wallet(GlobalBaseModel):
    wallet_ref = models.CharField(max_length=300)
    wallet_name = models.CharField(max_length=300)
    balance = models.FloatField(default=0.00)
    available_balance = models.FloatField(default=0.00)
    lien_amount = models.FloatField(default=0.00)
    allow_overdraw = models.BooleanField(default=False)
    status = models.CharField(max_length=300)
    scheme_code = models.CharField(max_length=300, default="000")
    post_deposit_calls = models.BooleanField(default=False)
    post_withdraw_calls = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @transaction.atomic()
    def deposit(self, amount=None, transaction_ref=None, narration=None, **kwargs):
        if amount <= 0:
            return {
                "success": False,
                "message": "Sorry cannot transact amounts less than 0",
            }
        else:
            if not self.get_action_recorder():
                return {
                    "success": False,
                    "message": "Sorry wallet records not defined ",
                }
            else:
                if not narration:
                    narration = "Deposit to account"
                prev_wlt_bal = self.balance
                self.balance += amount
                self.available_balance = self.balance - self.lien_amount
                new_wlt_bal = self.balance
                self.save()
                action_recorder = self.get_action_recorder()
                action_id = action_recorder.record_deposit(
                    amount=amount,
                    transaction_ref=transaction_ref,
                    wallet_ref=self.wallet_ref,
                    narration=narration,
                    wallet_bal=self.balance
                )
                signals.wallet_credited.send(sender=self.wallet_ref,amount=amount, trans_ref=transaction_ref, **kwargs)
                self.post_deposit(
                    transaction_ref=transaction_ref,
                    wlt_record_id=action_id,
                    amount=amount,
                    **kwargs
                )
                return {
                    "success": True,
                    "prev_wlt_bal": prev_wlt_bal,
                    "new_wlt_bal": new_wlt_bal,
                    "wlt_record_id": action_id,
                }

    """To DO implement it """

    def post_deposit(self, transaction_ref=None, wlt_record_id=None, amount=None):
        if not self.post_deposit_calls:
            pass
        else:
            pass

    def can_debit(self, amount=None):
        # check for fees and charges
        # Check the rights 
        deductions = get_withdrawal_deductions(wallet=None, amount=amount)
        total_debit_amount = deductions['total_deductions'] + amount
        if total_debit_amount > self.available_balance:
            return {"status": 1, "message": f"Insufficent funds available to carry out the transaction{total_debit_amount}"}
        return {"status": 0, "message": ""}

    def withdraw(
        self,
        amount=None,
        overdraw=False,
        transaction_ref=None,
        narration=None,
        **kwargs
    ):
        if amount <= 0:
            return {
                "success": False,
                "message": "Sorry cannot withdray amounts less than 0",
            }
        else:
            if amount > self.available_balance and overdraw is False:
                return {
                    "success": False,
                    "message": "Sorry cannot withdray amounts greater than the available balance",
                }
            else:
                if not narration:
                    narration = "Withdrawal from account"
                prev_wlt_bal = self.balance
                self.balance = prev_wlt_bal - amount
                self.available_balance = prev_wlt_bal - amount - self.lien_amount
                next_wlt_bal = self.balance
                self.save()
                action_recorder = self.get_action_recorder()
                action_id = action_recorder.record_wirdrawal(
                    amount=amount,
                    transaction_ref=transaction_ref,
                    wallet_ref=self.wallet_ref,
                    narration=narration,
                    wallet_bal=next_wlt_bal
                )   
                
                return {
                    "success": True,
                    "prev_wlt_bal": prev_wlt_bal,
                    "next_wlt_bal": next_wlt_bal,
                    "wlt_record_id": action_id,
                }

    def debit(self,amount=None,overdraw=False,transaction_ref=None,narration=None,**kwargs):
        if amount <= 0:
            return {
                "success": False,
                "message": "Sorry cannot withdray amounts less than 0",
            }
        else:
            if amount > self.available_balance and overdraw is False:
                return {
                    "success": False,
                    "message": "Sorry cannot withdray amounts greater than the available balance",
                }
            else:
                if not narration:
                    narration = "Withdrawal from account"
                prev_wlt_bal = self.balance
                self.balance = prev_wlt_bal - amount
                self.available_balance = prev_wlt_bal - amount - self.lien_amount
                next_wlt_bal = self.balance
                self.save()
                action_recorder = self.get_action_recorder()
                action_id = action_recorder.record_wirdrawal(
                    amount=amount,
                    transaction_ref=transaction_ref,
                    wallet_ref=self.wallet_ref,
                    narration=narration,
                    wallet_bal=next_wlt_bal
                )
                return {
                    "success": True,
                    "prev_wlt_bal": prev_wlt_bal,
                    "next_wlt_bal": next_wlt_bal,
                    "wlt_record_id": action_id,
                }


    def withdraw2(self,amount=None,overdraw=False, transaction_ref=None, narration=None, **kwargs ):
            chargable = kwargs["chargable"]
            if not chargable:
                self.debit(self,amount=amount,overdraw=overdraw,transaction_ref=transaction_ref,narration=narration,**kwargs)
            charge_mode = kwargs["charge_mode"]
            deductions = get_withdrawal_deductions(wallet=None, amount=amount)
            total_debit_amount = deductions['total_deductions'] + amount
            if total_debit_amount > self.available_balance:
                return {"status": 1, "message": f"Insufficent funds available to carry out the transaction{total_debit_amount}"}
            return {"status": 0, "message": ""}


    def add_lien(self, amount=None):
        if amount <= 0:
            return {
                "success": False,
                "message": "Sorry cannot transact amounts less than 0",
            }
        else:
            self.lien_amount = self.lien_amount + amount
            self.available_balance = self.balance - self.lien_amount
            self.save()

    def release_lien(self, amount=None):
        if amount <= 0:
            return "Sorry cannot transact amounts less than 0"
        else:
            if amount > self.lien_amount:
                pass
            else:
                self.lien_amount = self.lien_amount - amount
                self.available_balance = self.balance + amount
                self.save()

    def freeze(self):
        pass


class WalletRecords(models.Model):
    wallet_ref = models.CharField(max_length=500, blank=True, null=True)
    record_type = models.CharField(max_length=300, blank=True, null=True)
    record_amount = models.FloatField(default=0.00)
    transaction_ref = models.CharField(max_length=300, blank=True, null=True)
    narration = models.CharField(max_length=500, blank=True, null=True)
    wallet_balance = models.FloatField(default=0.00)
    related_source = models.CharField(max_length=500, blank=True, null=True)
    related_source_ref = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        abstract = True

    def record_deposit(self, amount=None, transaction_ref=None, narration=None, wallet_ref=None, wallet_bal=None):
        self.record_type = "CRE"
        self.record_amount = amount
        self.transaction_ref = transaction_ref
        self.narration = narration
        self.wallet_ref = wallet_ref
        self.wallet_balance = wallet_bal
        self.save()
        return self.id

    def record_wirdrawal(self, amount=None, transaction_ref=None, narration=None, wallet_ref=None, wallet_bal=None):
        self.record_type = "DEB"
        self.record_amount = amount
        self.transaction_ref = transaction_ref
        self.narration = narration
        self.wallet_ref = wallet_ref
        self.wallet_balance = wallet_bal
        self.save()
        return self.id


class NormalWalletRecords(WalletRecords):
    pass


class LoanWalletRecords(WalletRecords):
    pass


class LedgerWalletRecords(WalletRecords):
    pass


class NormalWallet(Wallet):
    cin = models.ManyToManyField(CINRegistry)

    def get_action_recorder(self):
        return NormalWalletRecords()


class LoanWallet(Wallet):
    cin = models.ManyToManyField(CINRegistry)

    def get_action_recorder(self):
        return LoanWalletRecords()


class LedgerWallet(Wallet):
    cin = models.ForeignKey(CINRegistry, on_delete=models.CASCADE, blank=True, null=True) 

    def get_action_recorder(self):
        return LedgerWalletRecords()

    
    def get_transaction_record(self, client_ref=None, wallet_record_id=None):
        return LedgerWalletRecords.objects.get(id=wallet_record_id)

class LoansDirectory(Wallet):
    loan_ref = models.CharField(max_length=300, blank=True, null=True)
    loan_wallet = models.OneToOneField(
        LoanWallet, on_delete=models.CASCADE, primary_key=True
    )


def wallet_search(wallet_ref=None, return_wallet=True, select_for_update=False):
    if NormalWallet.objects.filter(wallet_ref=wallet_ref).exists():
        if return_wallet and select_for_update:
            wallet = NormalWallet.objects.select_for_update().get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        elif return_wallet:
            wallet = NormalWallet.objects.get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        else:
            return {"status": 0, "message": "Normal Wallet exists"}

    elif LoanWallet.objects.filter(wallet_ref=wallet_ref).exists():
        if return_wallet and select_for_update:
            wallet = LoanWallet.objects.select_for_update().get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        elif return_wallet:
            wallet = LoanWallet.objects.get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        else:
            return {"status": 0, "message": "Loan Wallet exists"}

    elif LedgerWallet.objects.filter(wallet_ref=wallet_ref).exists():
        if return_wallet and select_for_update:
            wallet = LedgerWallet.objects.select_for_update().get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        elif return_wallet:
            wallet = LedgerWallet.objects.get(wallet_ref=wallet_ref)
            return {"status": 0, "wallet": wallet}
        else:
            return {"status": 0, "message": "Ledger Wallet exists"}
    else:
        return {"status": 1, "message": "Wallet does not exist"}


class Transactions(models.Model):
    transaction_ref = models.CharField(max_length=300, blank=True, null=True)
    debit_part_trans = models.IntegerField(default=1, blank=True, null=True)
    credit_part_trans = models.IntegerField(default=1, blank=True, null=True)
    initiated_by = models.CharField(max_length=300, blank=True, null=True)
    approved_by = models.CharField(max_length=300, blank=True, null=True)

    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def transact(
        self,
        debit_wallet_ref=None,
        credit_wallet_ref=None,
        amount=None,
        debit_narration=None,
        credit_narration=None,
        **kwargs
    ):

        amount = float(amount)
        if amount <= 0:
            return {
                "success": False,
                "message": "Sorry cannot transact amounts less than 0",
            }
        else:
            """get wallets"""
            debit_wallet_search = wallet_search(debit_wallet_ref)
            credit_wallet_search = wallet_search(credit_wallet_ref)
            if debit_wallet_search["status"] > 0 or credit_wallet_search["status"] > 0:
                return {
                    "success": False,
                    "message": "Sorry cannot transact amounts less than 0",
                }
            else:

                with transaction.atomic():
                    """Debit Part"""
                    transaction_ref = "".join(
                        choice(ascii_uppercase) for i in range(18)
                    )
                    self.transaction_ref = transaction_ref

                    debit_wallet = debit_wallet_search["wallet"]
                    debit_trans_records = debit_wallet.withdraw(
                        amount=amount,
                        overdraw=True,
                        transaction_ref=transaction_ref,
                        narration=debit_narration,
                        **kwargs
                    )
                    debit_trans_record_id = debit_trans_records["wlt_record_id"]
                    debit_transaction_records = TransactionsRecords()
                    debit_transaction_records.record_part_tran(
                        transaction_ref=transaction_ref,
                        wallet_ref=debit_wallet_ref,
                        wallet_record_id=debit_trans_record_id,
                        wallet_action="DEB",
                    )

                    """Credit Part"""
                    credit_wallet = credit_wallet_search["wallet"]
                    credit_trans_records = credit_wallet.deposit(
                        amount=amount,
                        transaction_ref=transaction_ref,
                        narration=credit_narration,
                        **kwargs
                    )
                    credit_trans_record_id = credit_trans_records["wlt_record_id"]

                    credit_transaction_records = TransactionsRecords()
                    credit_transaction_records.record_part_tran(
                        transaction_ref=transaction_ref,
                        wallet_ref=credit_wallet_ref,
                        wallet_record_id=credit_trans_record_id,
                        wallet_action="CRE",
                    )
                    self.save()

    """Single debit multiple credits"""

    def batch_credit(
        self,
        debit_wallet_ref=None,
        debit_amount=None,
        debit_narration=None,
        overdraw=None,
        credit_details=None,
        batch_credit_narration=None,
        allow_partial_processing=False,
        **kwargs
    ):
        credit_sum = sum_batch_records(batch_list=credit_details)
        if credit_sum != debit_amount:
            return {"status": 1, "message": "Sorry Transaction imbalanced"}
        else:
            """Check wallet validiy"""
            debit_wallet_search = wallet_search(wallet_ref=debit_wallet_ref)

            if debit_wallet_search["status"] != 0:
                return {"status": 1, "message": "Sorry debit wallet does not exist"}
            else:
                existing_wallets = []
                missing_wallets = []
                for credit_detail in credit_details:
                    wlt_search_rslt = wallet_search(
                        wallet_ref=credit_detail["wallet_ref"],
                        return_wallet=False,
                        select_for_update=False,
                    )
                    if wlt_search_rslt["status"] != 0:
                        missing_wallets.append(credit_detail)
                    else:
                        existing_wallets.append(credit_detail)
                if not missing_wallets:
                    with transaction.atomic():
                        """Debit Part"""
                        trans_sum = sum_batch_records(batch_list=credit_details)
                        transaction_ref = "".join(
                            choice(ascii_uppercase) for i in range(18)
                        )
                        self.transaction_ref = transaction_ref

                        debit_wallet = debit_wallet_search["wallet"]
                        debit_trans_records = debit_wallet.withdraw(
                            amount=trans_sum,
                            overdraw=True,
                            transaction_ref=transaction_ref,
                            narration=debit_narration,
                        )
                        debit_trans_record_id = debit_trans_records["wlt_record_id"]
                        debit_transaction_records = TransactionsRecords()
                        debit_transaction_records.record_part_tran(
                            transaction_ref=transaction_ref,
                            wallet_ref=debit_wallet_ref,
                            wallet_record_id=debit_trans_record_id,
                            wallet_action="DEB",
                        )

                        batch_sum = 0.0

                        for wallet_details in existing_wallets:
                            narration = wallet_details.get("narration", None)
                            if not narration:
                                credit_narration = batch_credit_narration
                            else:
                                credit_narration = narration
                            credit_wallet_srch_dtls = wallet_search(
                                wallet_ref=wallet_details["wallet_ref"],
                                return_wallet=True,
                                select_for_update=True,
                            )
                            credit_wallet = credit_wallet_srch_dtls["wallet"]
                            credit_trans_records = credit_wallet.deposit(
                                amount=wallet_details["amount"],
                                transaction_ref=transaction_ref,
                                narration=credit_narration,
                                **kwargs
                            )
                            credit_trans_record_id = credit_trans_records[
                                "wlt_record_id"
                            ]

                            credit_transaction_records = TransactionsRecords()
                            credit_transaction_records.record_part_tran(
                                transaction_ref=transaction_ref,
                                wallet_ref=wallet_details["wallet_ref"],
                                wallet_record_id=credit_trans_record_id,
                                wallet_action="CRE",
                            )
                            self.save()
                            batch_sum += wallet_details["amount"]
                    return {"status": 0, "message": "Batch process succesful"}


class TransactionsRecords(models.Model):
    transaction_ref = models.CharField(max_length=300, blank=True, null=True)
    wallet_ref = models.CharField(max_length=300, blank=True, null=True)
    wallet_action = models.CharField(max_length=300, blank=True, null=True)
    wallet_record_id = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def record_part_tran(
        self,
        transaction_ref=None,
        wallet_ref=None,
        wallet_record_id=None,
        wallet_action=None,
    ):
        self.transaction_ref = transaction_ref
        self.wallet_ref = wallet_ref
        self.wallet_record_id = wallet_record_id
        self.wallet_action = wallet_action
        self.save()


def sum_batch_records(batch_list=None):
    batch_sum = 0.0
    for batch_item in batch_list:
        batch_sum += batch_item["amount"]
    return batch_sum



def get_withdrawal_deductions(wallet=None):
    """To do- get the charges from the code and the account"""
    scheme_code = wallet.scheme_code
    withdrwl_fee = 10
    withdrwl_penalty = 200
    total_deductions = withdrwl_fee + withdrwl_penalty
    return {"withdrawal_fee": withdrwl_fee, "withdrwl_penalty": withdrwl_penalty, "total_deductions": total_deductions}
