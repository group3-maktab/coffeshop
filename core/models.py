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