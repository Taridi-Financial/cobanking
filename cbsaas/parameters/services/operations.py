from cbsaas.parameters.models import ClientWalletDirectory


def add_specific_GLs():
    pass


def get_wallet_from_code(client_ref=None, use_type_code=None, branch_code=None):
    if not branch_code:
        try:
            wallet = ClientWalletDirectory.objects.get(
                client_ref=client_ref, use_type_code=use_type_code, branch_code=000
            )
        except Exception:
            return {"status": 1, "message": "wallet does not exist"}
        else:
            return {"status": 0, "wallet": wallet}
    else:
        try:
            wallet = ClientWalletDirectory.objects.get(
                client_ref=client_ref,
                use_type_code=use_type_code,
                branch_code=branch_code,
            )
        except Exception:
            return {"status": 1, "message": "wallet does not exist"}
        else:
            return {"status": 0, "wallet": wallet}


def add_wallet_for_code_type(
    wallet_ref=None,
    client_ref=None,
    use_type_code=None,
    description=None,
    branch_code=None,
    update=False,
):
    if not branch_code:
        return {"status": 1, "message": "Kindly provice the code"}
    else:
        try:
            wallet = ClientWalletDirectory.objects.get(
                client_ref=client_ref,
                use_type_code=use_type_code,
                branch_code=branch_code,
            )
        except Exception:
            wallet = ClientWalletDirectory.objects.create(
                wallet_ref=wallet_ref,
                use_type_code=use_type_code,
                wallet_description=description,
                client_ref=client_ref,
            )
            return {
                "status": 0,
                "wallet": wallet,
                "message": "Parameter added successfully",
            }
        else:
            return {"status": 1, "message": "wallet does not exist"}
