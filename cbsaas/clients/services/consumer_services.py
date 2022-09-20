import random

from ..models import ConsumerRegistry


def consumers_create_consumer(client_id=None, consumer_national_no=None, owner_type=None):
    owner_types = ["CLIENT", "USER", "SERVICEPROVIDER"]
    if not owner_type in owner_types:
        return {"status": 1, "message": f"Wrong owner type provided, owner types are {owner_types}"}

    existing_consumer = consumers_get_or_check_nn(client_id=client_id, consumer_national_no=consumer_national_no, owner_type=owner_type)
    if existing_consumer:
        return {"status": 1, "message": "Consumer with that number already exists"}
    
    consumer_number = consumers_generate_consumer_no(client_id=None) 
    new_consumer = ConsumerRegistry.objects.create(consumer_national_no=consumer_number, consumer_type = owner_type, client_id=client_id)
    return {
        "status": 0,
        "consumer_system_no": new_consumer.consumer_system_no,
        "consumer_id": new_consumer.id,
        "consumer_sn": new_consumer.consumer_system_no,
        "message": "Consumer added successfully",
    }

def consumers_generate_consumer_no(client_id=None):
    return random.randint(1000, 10000)

def consumers_get_or_check_nn(client_id=None, consumer_national_no=None, owner_type=None, request_type=None, get_pk=False):
    if request_type == "get":
        consumer = ConsumerRegistry.objectstenant_querry(client_id=client_id).filter(consumer_national_no=consumer_national_no, owner_type=owner_type).first()
        if consumer:
            if get_pk:
                return consumer.pk
            return consumer
        else:
            return None
    else:
        if ConsumerRegistry.objectstenant_querry(client_id=client_id).filter(consumer_national_no=consumer_national_no, owner_type=owner_type).exists():
            return True
        return False

def consumers_get_or_check_sn(client_id=None, consumer_system_no=None, is_check_rqst=False, get_pk=False):
    """sn statnds for system_no
    rtype: ccnsumer instance"""
    if not is_check_rqst:
        consumer = ConsumerRegistry.objectstenant_querry(client_id=client_id).filter(consumer_system_no=consumer_system_no).first()
        if consumer:
            if get_pk:
                return consumer.pk
            return consumer
        else:
            return None
    else:
        if ConsumerRegistry.objectstenant_querry(client_id=client_id).filter(consumer_system_no=consumer_system_no).exists():
            return True
        return False

