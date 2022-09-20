from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from cbsaas.clients.models import Clients
from cbsaas.ibase.models import GlobalBaseModel

from cbsaas.cin.models import ConsumerRegistry
from cbsaas.ibase.tenantmodels import TenantBaseModel
class User(AbstractUser):
    """
    Default custom user model for cbsaas.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = models.CharField(max_length=255)
    USERNAME_FIELD: email
    client = models.ForeignKey(Clients, on_delete=models.SET_NULL)
    consumer = models.OneToOneField(ConsumerRegistry, on_delete=models.SET_NULL) 
    gender = models.CharField(max_length=1000,blank=True,null=True)
    phone = models.CharField(max_length=100,blank=True,null=True) 
    DOB = models.DateField()
    marital_status = models.CharField(max_length=100,blank=True,null=True)
    pin = models.CharField(max_length=100,blank=True, null=True)
    session_mode = models.CharField(max_length=100,default=0,blank=True,null=True) #staff, user, provider

    first_name = None  # type: ignore
    last_name = None  # type: ignore
    # username = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view. 
        Returns: str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})

    def set_pin(self, pin=None):
        pass

    def reset_pin(self):
        pass

    def verify_pin(self, pin=None):
        pass

class Staff(TenantBaseModel):  
    user = models.OneToOneField(User, on_delete=models.SET_NULL)
    staff_id = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    designation = models.CharField(max_length=100,blank=True,null=True) #manager, ceo

class Members(TenantBaseModel):  
    user = models.OneToOneField(User, on_delete=models.SET_NULL)
    membership_no= models.CharField(max_length=100,blank=True,null=True)
    status = models.CharField(max_length=100,default=0,blank=True,null=True) 
    

class TempUsers(TenantBaseModel):  
    action = models.CharField(max_length=100,blank=True, null=True) #new edit, delete
    instance_id = models.CharField(max_length=100,blank=True,null=True)
    made_by = models.CharField(max_length=100,blank=True,null=True) 
    checked_by = models.CharField(max_length=100,blank=True,null=True) 
    status = models.CharField(max_length=100,default=0,blank=True,null=True) #enter, approved, rejected
    user_type = models.CharField(max_length=100,default=0,blank=True,null=True) #member, staff
    first_name = models.CharField(max_length=100,blank=True, null=True) 
    last_name = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True) 
    staff_or_member_no= models.CharField(max_length=100,blank=True,null=True)
    physical_address = models.CharField(max_length=100,default=0,blank=True,null=True) 
    gender = models.CharField(max_length=1000,blank=True,null=True)
    DOB = models.CharField(max_length=1000,blank=True,null=True)
    marital_status = models.CharField(max_length=100,default=0,blank=True,null=True)

class UserContacts(TenantBaseModel):  
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=100,blank=True,null=True) 
    email = models.CharField(max_length=255)
    physical_address = models.CharField(max_length=100,default=0,blank=True,null=True)

