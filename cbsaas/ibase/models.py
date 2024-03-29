from datetime import timezone
from django.db import models

"""Meant to implement soft delete"""


class GlobalBaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def tenant_querry(self, client_id=None):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def gen_querry(self):
        """For client querries. for objects without client relation by default"""
        return super().get_queryset().filter(deleted_at__isnull=True)


class GlobalBaseModel(models.Model):
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    objects = GlobalBaseManager()
    all_objects = models.Manager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        self.delete()

    def restore(self):
        self.deleted_at = None
        self.save()
    class Meta:
        abstract = True


class BaseModel(models.Model):
    creation_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    objects = GlobalBaseManager()
    all_objects = models.Manager()

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        self.delete()

    def restore(self):
        self.deleted_at = None
        self.save()
    class Meta:
        abstract = True


