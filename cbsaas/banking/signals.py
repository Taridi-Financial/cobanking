from django import dispatch

wallet_credited = dispatch.Signal(providing_args=[" amount, trans_ref"]) #sender is wallet ref