from django.db import models
from cbsaas.clients.models import Clients
from cbsaas.ibase.models import GlobalBaseModel


class BaseCustomer(GlobalBaseModel):  
    first_name = models.CharField(max_length=100,blank=True, null=True) 
    last_name = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True) 
    phone = models.CharField(max_length=100) 
    physical_address = models.CharField(max_length=100,default=0,blank=True,null=True) 
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Customers(BaseCustomer):  
    pass
    

class TempCustomers(BaseCustomer):  
    type = models.CharField(max_length=100,blank=True, null=True) #new edit, delete
    instance_id = models.CharField(max_length=100,blank=True,null=True)
    made_by = models.CharField(max_length=100,blank=True,null=True) 
    checked_by = models.CharField(max_length=100,blank=True,null=True) 
    status = models.CharField(max_length=100,default=0,blank=True,null=True) #enter, approved, rejected