import uuid
from django.db import models

from cbsaas.ibase.models import GlobalBaseModel
from cbsaas.ibase.tenantmodels import TenantBaseModel


class Clients(GlobalBaseModel):
    client_ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client_name = models.CharField(max_length=225)
    client_code = models.CharField(max_length=100)  #to be attached to the accounts 
    address = models.CharField(max_length=100)


# default branch main.. code 000
class Branches(TenantBaseModel):
    branch_name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    updated_at = models.DateTimeField()


class ConsumerRegistry(TenantBaseModel):
    consumer_system_no = models.CharField(max_length=300)
    consumer_national_no = models.CharField(max_length=300)
    consumer_name = models.CharField(max_length=300)
    consumer_type = models.CharField(max_length=100)
    """consumer types, USER, CLIENT, BUSINESS, SERVICEPROVIDER """
    """Unique true with client ref and identifying number """
    status = models.CharField(max_length=100)


class ClientWalletDirectory(TenantBaseModel):
    wallet_ref = models.CharField(max_length=300, blank=True, null=True)
    use_type_code = models.CharField(max_length=300, blank=True, null=True)
    branch_code = models.CharField(max_length=300, blank=True, null=True)
    wallet_name = models.CharField(max_length=300, blank=True, null=True)
    wallet_description = models.CharField(max_length=300, blank=True, null=True)
    client_ref = models.CharField(max_length=300, blank=True, null=True)
    use_level = models.CharField(
        max_length=300, blank=True, null=True
    )  # global, branch if global its only one, if branch it can be replicated