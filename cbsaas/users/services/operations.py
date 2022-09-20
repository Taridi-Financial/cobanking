


from cbsaas.cin.services.operations import get_consumer
from cbsaas.lending.models import User
from cbsaas.users.models import Members, Staff


class UserOperations:   
    def __init__(self,**kwargs) -> None:
        self.__dict__.update(kwargs)
        self.operation_status = 0
        self.response_msg = None
        self.response_status = 0
        """Arguments list
        To create new client :
        identifying_number=None, client_name = None, address=None, superadmin_email=None
        """  

    def create_user_obj(self):
        pass
    def set_consumer(self):
        consumer = get_consumer(consumer_number=self.consumer_number, client_id=self.client_id, consumer_type='USER')
        if not consumer:
            self.operation_status = 0
            self.response_msg = 'Sorry consumer with that number does not exist'

    def create_user_obj(self):
        new_user = User.objects.create_user(
            username=self.email, 
            email=self.email, 
            name=self.consumer.consumer_name, 
            consumer_id=self.consumer.id,
            password="", 
            is_active=False,
            phone=self.phone,
            gender=self.gender,
            marital_status=self.marital_status,
            DOB=self.DOB
        )
        self.new_user = self.new_user

        # if self.user_type == "staff":
        #     self.create_staff()
        # else:
        #     self.create_member()

    def create_staff_obj(self):
        Staff.objects.create(client_id=self.client_id,user_id=self.new_user.id, staff_id=self.staff_or_member_no)

    def create_member_obj(self):
        Members.objects.create(client_id=self.client_id,user_id=self.new_user.id, membership_no=self.staff_or_member_no)


def users_create_user(client_id=None,consumer_system_no=None,user_type =None,email=None,phone=None,staff_or_member_no=None,gender = None, DOB =None):
    user_ops = UserOperations(client_id=None,consumer_number=None,user_type =None,email=None,phone=None,staff_or_member_no=None,gender = None, DOB =None)