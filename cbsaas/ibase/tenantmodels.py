from django.db import models

from cbsaas.ibase.models import BaseModel
from cbsaas.clients.models import Clients


class TenantBaseModel(BaseModel):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    class Meta:
        abstract = True