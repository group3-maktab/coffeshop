from django.conf import settings
from django.utils import timezone

from django.db import models

"""
https://github.com/Dineshs91/soft-delete-options-in-django
"""


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # Exclude soft-deleted items by default
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10)  # 'CREATE', 'UPDATE', 'DELETE'
    timestamp = models.DateTimeField(auto_now_add=True)
    table_name = models.CharField(max_length=50)
    row_id = models.TextField()
    old_value = models.JSONField(null=True)