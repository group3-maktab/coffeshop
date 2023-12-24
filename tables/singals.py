from django.db.models.signals import post_migrate
from django.dispatch import receiver

from tables.models import Table


@receiver(post_migrate)
def create_default_tags(sender, **kwargs):
    if not Table.objects.filter(status='T').exists():
        Table.objects.create(number=0, status='T')
