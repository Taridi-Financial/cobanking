import random

from ..models import CINRegistry


def get_cin(identifying_number=None, client_id=None, owner_type=None):
    if not client_id:
        if CINRegistry.objects.filter(
            identifying_number=identifying_number, owner_type=owner_type
        ).exists():
            cin = CINRegistry.objects.filter(
                identifying_number=identifying_number, owner_type=owner_type
            ).first()
            return {
                "status": 0,
                "cin": cin.cin,
                "message": "Cin retrieved successfully",
            }
        else:
            return {"status": 1, "message": "Cin does not exist"}
    else:

        if CINRegistry.objects.filter(
            client_id=client_id,
            identifying_number=identifying_number,
            owner_type=owner_type,
        ).exists():
            cin = CINRegistry.objects.filter(
                client_id=client_id,
                identifying_number=identifying_number,
                owner_type=owner_type,
            ).first()
            return {
                "status": 0,
                "cin": cin.cin,
                "message": "Cin retrieved successfully",
            }
        else:
            return {"status": 1, "message": "Cin does not exist"}


def generate_cin(client_id=None, identifying_number=None, owner_type=None):
    cin_status = get_cin(
        client_id=client_id,
        identifying_number=identifying_number,
        owner_type=owner_type,
    )
    if cin_status["status"] == 0:
        return {"status": 1, "message": "Cin exists", "cin": cin_status["cin"]}
    else:
        if owner_type == "CLIENT":
            new_cin = CINRegistry()
            new_cin.cin = random.randint(1000, 10000)
            new_cin.identifying_number = identifying_number
            new_cin.owner_type = owner_type
            new_cin.save()
            return {
                "status": 0,
                "cin": new_cin.cin,
                "message": "Cin added successfully",
            }

        # elif owner_type == "USER":
        #     new_cin = CINRegistry()
        #     new_cin.cin = random.randint(1000, 10000)
        #     new_cin.identifying_number = identifying_number
        #     new_cin.owner_type = owner_type
        #     new_cin.save()
        #     return {"status":0, "cin":new_cin.cin, "message":'Cin added successfully'}

        # else:
        #     new_cin = CINRegistry()
        #     new_cin.cin = random.randint(1000, 10000)
        #     new_cin.identifying_number = identifying_number
        #     new_cin.owner_type = owner_type
        #     new_cin.save()
        #     return {"status":0, "cin":new_cin.cin, "message":'Cin added successfully'}


def update_cin_with_client_ref(client_ref=None, cin=None):
    try:
        cin_reg = CINRegistry.objects.get(cin=cin)
    except Exception:
        pass
    else:
        cin_reg.client_ref = client_ref
        cin_reg.save()


def get_client_cin(client_ref=None):
    cin_reg = CINRegistry.objects.filter(client_ref=client_ref).first()

    return {"status": 0, "cin": cin_reg.cin, "message": "Cin retrieved successfully"}
