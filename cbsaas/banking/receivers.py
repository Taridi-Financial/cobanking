
from django.dispatch import receiver
from . import signals


@receiver(signals.wallet_credited)
def wallet_credited_receiver(sender, amount, trans_ref, **kwargs):
    print('fffffffffffffffffffffhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    print(sender, amount)
    ght = kwargs.get('vanila', 'Badman')
    print(ght)