import uuid

from django.db import models

from cbsaas.ibase.models import GlobalBaseModel


class Clients(GlobalBaseModel):
    client_ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client_name = models.CharField(max_length=225)
    identifying_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)


# default branch main.. code 000
class Branches(GlobalBaseModel):
    branch_name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
