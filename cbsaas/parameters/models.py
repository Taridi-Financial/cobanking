from django.db import models

from cbsaas.ibase.models import GlobalBaseModel


class ClientWalletDirectory(GlobalBaseModel):
    wallet_ref = models.CharField(max_length=300, blank=True, null=True)
    use_type_code = models.CharField(max_length=300, blank=True, null=True)
    branch_code = models.CharField(max_length=300, blank=True, null=True)
    wallet_name = models.CharField(max_length=300, blank=True, null=True)
    wallet_description = models.CharField(max_length=300, blank=True, null=True)
    client_ref = models.CharField(max_length=300, blank=True, null=True)
    use_level = models.CharField(
        max_length=300, blank=True, null=True
    )  # global, branch if global its only one, if branch it can be replicated
