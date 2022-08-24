from django import dispatch

wallet_credited = dispatch.Signal(providing_args=[" amount, trans_ref, wallet_record_id"]) #sender is wallet