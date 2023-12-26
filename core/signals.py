from core.models import AuditLog
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save, pre_delete
from foodmenu.models import Food,Category
from tag.models import Tag,TaggedItem
from tables.models import Table, Reservation
from order.models import Order, OrderItem


@receiver(post_save, sender=Food)
@receiver(post_save, sender=Category)
@receiver(post_save, sender=Tag)
@receiver(post_save, sender=TaggedItem)
@receiver(post_save, sender=Table)
@receiver(post_save, sender=Reservation)
@receiver(post_save, sender=Reservation)
@receiver(post_save, sender=Order)
@receiver(post_save, sender=OrderItem)
def log_create_update(sender, instance, created, **kwargs):
    model_name = sender.__name__


    if created:
        action = 'CREATE'
        # old_value = None
    else:
        action = 'UPDATE'
        # # old_value = {field.name: getattr(instance, field.name) for field in instance._meta.fields}
        # old_value = None

    table_name = sender._meta.db_table
    row_id = instance.id
    user = instance.user if hasattr(instance, 'user') else None

    AuditLog.objects.create(
        user=user,
        action=action,
        table_name=table_name,
        row_id=row_id,
        # old_value=# old_value,
    )

@receiver(pre_delete, sender=Food)
@receiver(pre_delete, sender=Category)
@receiver(pre_delete, sender=Tag)
@receiver(pre_delete, sender=TaggedItem)
@receiver(pre_delete, sender=Table)
@receiver(pre_delete, sender=Reservation)
@receiver(pre_delete, sender=Reservation)
@receiver(pre_delete, sender=Order)
@receiver(pre_delete, sender=OrderItem)
def log_delete(sender, instance, **kwargs):
    model_name = sender.__name__
    if isinstance(instance, Session) or isinstance(instance, AuditLog):
        return

    table_name = sender._meta.db_table
    row_id = instance.id
    user = instance.user if hasattr(instance, 'user') else None

    AuditLog.objects.create(
        user=user,
        action='DELETE',
        table_name=table_name,
        row_id=row_id,
        # old_value=None,
    )