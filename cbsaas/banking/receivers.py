
from django.dispatch import receiver
from cbsaas.payments.services.operations import record_payments_transaction_monitor

from . import signals


@receiver(signals.wallet_credited)
def wallet_credited_receiver(sender, amount, trans_ref,wallet_record_id, **kwargs):
    """Decide the different services for Process payments for payment attached wallets"""
    record_payments_transaction_monitor(sender, amount, trans_ref,wallet_record_id, **kwargs)
    """(TO DO send_messaging(sender, amount, trans_ref,wallet_record_id, **kwargs)"""
