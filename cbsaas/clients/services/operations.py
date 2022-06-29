from cbsaas.cin.services.operations import (
    generate_cin,
    get_cin,
    update_cin_with_client_ref,
)
from cbsaas.clients.models import Branches, Clients


def add_client(client_name=None, address=None, identifying_number=None):
    cin_check = get_cin(identifying_number=identifying_number, owner_type="CLIENT")
    if cin_check["status"] == 0:
        return {
            "status": 1,
            "message": "Sorry the number already has a cin",
            "cin": cin_check["cin"],
        }
    else:
        new_cin = generate_cin(
            client_id=None, identifying_number=identifying_number, owner_type="CLIENT"
        )
        cin = new_cin["cin"]
        if new_cin["status"] == 0:
            new_client = Clients.objects.create(
                client_name=client_name,
                address=address,
                identifying_number=identifying_number,
            )
            update_cin_with_client_ref(client_ref=new_client.client_ref, cin=cin)
            default_branch = Branches()

            default_branch.branch_name = "Main"
            default_branch.branch_code = 000
            default_branch.status = "Active"
            default_branch.client = new_client
            default_branch.save()
            return {
                "status": 0,
                "message": "New client created successfully",
                "cin": cin,
                "client_ref": new_client.client_ref,
            }
        else:
            return {"status": 1, "message": "failed"}
        # Scheme code
        #
        """Cash GL, Mpesa Incoming GL, Mpesa Outgoing GL,
        Bank account GL, Interest income GL, Other income GL,
        Interest expense GL"""


def add_client_params():
    pass
