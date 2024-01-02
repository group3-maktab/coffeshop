from decimal import Decimal
from core.models import AuditLog
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save, pre_delete
from foodmenu.models import Food,Category
from tag.models import Tag,TaggedItem
from tables.models import Table, Reservation
from order.models import Order, OrderItem
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.files import FileField
from django.db.models.fields import DateTimeField
import uuid
import inspect

""" 
   ________________________________________________________________________________
  |                   IF WE WANT TO ADD USER INTO DATABASE                         |    
  |                                                                                |
  |  pre_save_signal = Signal(providing_args=["instance", "request"])              |    
  |  post_save_signal = Signal(providing_args=["instance", "created", "request"])  |
  |                                                                                |    
  |  @receiver(post_save_signal, sender=Food)                                      |        
  |  def log_post_save(sender, instance, created, request, **kwargs):              |                
  |      user = request.user if request.user.is_authenticated else None            |        
   ________________________________________________________________________________
   
"""



def serialize_model_instance(instance):
    fields = {}
    for field in instance._meta.fields:
        print(field)
        field_value = getattr(instance, field.name)
        if isinstance(field, DateTimeField):
            field_value = field_value.isoformat() if field_value else None
        elif isinstance(field, ForeignKey):
            field_value = field_value.pk if field_value else None
        elif isinstance(field, FileField):
            continue
        elif isinstance(field_value, Decimal):
            field_value = str(field_value)
        elif isinstance(field_value, uuid.UUID):
            field_value = str(field_value)

        fields[field.name] = field_value

    return fields


@receiver(post_save, sender=Food)
@receiver(post_save, sender=Category)
@receiver(post_save, sender=Tag)
@receiver(post_save, sender=TaggedItem)
@receiver(post_save, sender=Table)
@receiver(post_save, sender=Reservation)
@receiver(post_save, sender=Reservation)
@receiver(post_save, sender=Order)
def log_create_update(sender, instance, created, **kwargs):
    model_name = sender.__name__  #just for fun :-|


    if created:
        action = 'CREATE'
        old_value = None
    else:
        action = 'UPDATE'
        old_value = serialize_model_instance(instance)

    table_name = sender._meta.db_table
    row_id = instance.id
    """                                                                                               """"""
    |                                                                                                   |        
    |        https://stackoverflow.com/questions/4721771/get-current-user-log-in-signal-in-django       |
    |                                                                                                   |
    """                                                                                               """"""
    # refrence is up here
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            """https://docs.python.org/3/library/inspect.html"""
            """https://www.geeksforgeeks.org/inspect-module-in-python/"""
            break

    user = request.user

    AuditLog.objects.create(
        user=user,
        action=action,
        table_name=table_name,
        row_id=row_id,
        old_value=old_value,
    )

@receiver(pre_delete, sender=Food)
@receiver(pre_delete, sender=Category)
@receiver(pre_delete, sender=Tag)
@receiver(pre_delete, sender=TaggedItem)
@receiver(pre_delete, sender=Table)
@receiver(pre_delete, sender=Reservation)
@receiver(pre_delete, sender=Reservation)
@receiver(pre_delete, sender=Order)
def log_delete(sender, instance, **kwargs):
    model_name = sender.__name__ #just for fun :-|
    if isinstance(instance, Session) or isinstance(instance, AuditLog):
        return

    table_name = sender._meta.db_table
    row_id = instance.id
    """                                                                                               """"""
    |                                                                                                   |        
    |        https://stackoverflow.com/questions/4721771/get-current-user-log-in-signal-in-django       |
    |                                                                                                   |
    """                                                                                               """"""
    # refrence is up here
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            """https://docs.python.org/3/library/inspect.html"""
            """https://www.geeksforgeeks.org/inspect-module-in-python/"""
            break

    user = request.user

    old_value = serialize_model_instance(instance)

    AuditLog.objects.create(
        user=user,
        action='DELETE',
        table_name=table_name,
        row_id=row_id,
        old_value=old_value,
    )