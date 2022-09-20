
from cbsaas.clients.models import Branches, Clients
from cbsaas.clients.services.consumer_services import consumers_create_consumer
from cbsaas.users.services.operations import users_create_user

class ClientOperations:   
    def __init__(self,**kwargs) -> None:
        self.__dict__.update(kwargs)
        self.operation_status = 0
        self.response_msg = None
        self.response_status = 0
        """Arguments list
        To create new client :
        identifying_number=None, client_name = None, address=None, superadmin_email=None, superadmin_national_id=None
        """  

    def create_client(self):
        self.can_create()
        if not self.operation_status > 0:
            self.save_new_client()
        if not self.operation_status > 0:
            self.create_branch(branch_name="Head Office", branch_code="000")
            self.create_branch(branch_name="Branch one", branch_code="001")
        if not self.operation_status > 0:
            self.create_superadmin()

    def can_create(self): 
        if Clients.objects.gen_querry.filter(identifying_number=self.identifying_number).exists():
            self.response_msg = 'Sorry, another client with the same number exists'
            self.operation_status = 1

    def save_new_client(self): 
        self.client = Clients.objects.create(
                client_name=self.client_name,
                address=self.address,
                identifying_number=self.identifying_number,
            )
        self.response_msg = 'Saving of new client successful'

    def create_branch(self,branch_name=None, branch_code=None):     
        Branches.objects.create(
                branch_name=branch_name,
                branch_code=branch_code,
                client_id=self.client.id,
                status="active"
            )

    def create_consumer(self, consumer_national_no=None, owner_type=None):
        consumer_msg = consumers_create_consumer(client_id=self.client_id, consumer_national_no=consumer_national_no, owner_type=owner_type)
        if not consumer_msg['status'] == 0:
            return None
        return consumer_msg

    def create_client_consumer(self):
        client_consumer_msg = self.create_consumer(consumer_national_no=self.superadmin_national_id, owner_type="CLIENT")
        if not client_consumer_msg["status"] ==0:
            self.operation_status = 1
            msg = client_consumer_msg["message"]
            self.response_msg = f"Could not create the client consumer reason: {msg}"
        self.response_msg = f"Client consumer created successfully "

    def create_superadmin(self): 
        """TO DO: Add staff of type superadmin.  email to create a user"""
        consumer_msg = self.create_consumer(consumer_national_no=self.superadmin_national_id, owner_type="USER")
        if not consumer_msg:
            pass
        new_user_msg = users_create_user(
            client_id=self.client_id,
            consumer_system_no=consumer_msg["consumer_sn"],
            user_type ="staff",email=self.superadminemail,
            phone=self.superadmin_phone,
            staff_or_member_no=self.staff_or_member_no,
            gender = self.gender, 
            DOB =self.DOB)
        if not new_user_msg["status"] ==0:
            self.operation_status = 1
            msg = new_user_msg["message"]
            self.response_msg = f"Could not create the superadmin reason: {msg}"
        self.response_msg = f"Superuser created successfully"


def get_client_from_ref(client_ref, only_pk=False):
    client = Clients.objects.filter(client_ref=client_ref).first()
    if only_pk:
        return client.pk
    return client