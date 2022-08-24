
from django.dispatch import receiver

from cbsaas.banking.services.payments import record_payments_transaction_monitor
from . import signals


@receiver(signals.wallet_credited)
def wallet_credited_receiver(sender, amount, trans_ref,wallet_record_id, **kwargs):
    print(wallet_record_id)
    record_payments_transaction_monitor(sender, amount, trans_ref,wallet_record_id, **kwargs)
