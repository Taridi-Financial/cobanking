from django.db import models

from cbsaas.ibase.models import GlobalBaseModel


class CINRegistry(GlobalBaseModel):
    cin = models.CharField(max_length=300, blank=True, null=True)
    client_ref = models.CharField(max_length=300, blank=True, null=True)
    identifying_number = models.CharField(max_length=300, blank=True, null=True)
    """Owner types, """
    owner_type = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
