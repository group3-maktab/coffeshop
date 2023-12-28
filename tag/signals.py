# signals.py
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_migrate, post_delete, pre_delete
from django.dispatch import receiver
from django.apps import AppConfig

from foodmenu.models import Food
from .models import Tag, TaggedItem
from utils import update_food_availability

"""
    Certainly! The @receiver decorator in Django is used to connect a function (receiver) to a signal. Here's a detailed explanation:


        @receiver(signal, sender=None, dispatch_uid=None)
        def receiver_function(sender, **kwargs):
            # Your code here
    
    
    Parameters:
        signal: The signal to which the receiver is connected.
        sender (optional): The sender for which the receiver should be triggered. If None, the receiver will be triggered for any sender of the signal.
        dispatch_uid (optional): A unique identifier for the receiver. If provided, it prevents duplicate receivers from being connected.
        How It Works:
        
            Connecting the Receiver to the Signal:
            You decorate a function with @receiver to connect it to a signal.
            The signal parameter specifies which signal the receiver should listen to.
            If sender is specified, the receiver will only be triggered when the signal is sent by the specified sender. If sender is None, the receiver will be triggered for any sender.
            
            Signature of the Receiver Function:
            The receiver function should have the signature def my_receiver(sender, **kwargs).
            The sender argument represents the sender of the signal.
            The **kwargs argument captures any additional keyword arguments sent with the signal.
            
            Executing Code in Response to the Signal:            
            When the signal is sent, the connected receiver function is executed.
            The sender and additional arguments are passed to the receiver function.
            
            Common Use Cases:
                Model Signals: Connect receiver functions to signals such as pre_save,
                 post_save, pre_delete, and post_delete to perform actions before or after model instances are saved or deleted.
                Custom Signals: Define custom signals and connect receivers to implement custom event handling within your application.
                
            When to Use:
                Use the @receiver decorator when you want to execute specific code in
                 response to certain events (signals) in your Django application.
                It promotes loose coupling between components,
                 allowing you to extend or modify behavior without modifying the sender.
"""


@receiver(post_save, sender=Tag)
def handle_tag_change(sender, instance, **kwargs):
    """
    Django signals are a mechanism that allows certain senders to notify
     a set of receivers that some action has taken place.
      This decouples the sender and receiver,
       making it easy to add or remove functionalities without modifying the sender.

In Django, signals are based on the Observer design pattern.
 The sender is the object that sends the signal,
  and the receiver is the function that gets executed when the signal is sent.
    """
    update_food_availability(instance)


@receiver(post_save, sender=TaggedItem)
@receiver(post_delete, sender=TaggedItem)
def handle_taggeditem_generated(sender, instance, **kwargs):
    try:
        taggeditem = TaggedItem.objects.get(pk=instance.pk)
        tag_id = taggeditem.tag_id
        update_food_availability(tag_id)
    except TaggedItem.DoesNotExist:
        Food.objects.update(availability=True)
        unavailable_tags = TaggedItem.objects.get_unavailable_tags(Food)
        content_type = ContentType.objects.get_for_model(Food)
        object_ids = [tag.object_id for tag in unavailable_tags if tag.content_type == content_type]
        food_objects = Food.objects.filter(id__in=object_ids)
        food_objects.update(availability=False)


@receiver(post_migrate)
def create_default_tags(sender, **kwargs):
        if not Tag.objects.filter(label='unavailable').exists():
            Tag.objects.create(label='unavailable', available=False)

"""
Signals and middleware are both concepts used in Django for different purposes,
 and they serve distinct roles in the framework.

    Signal:
    
        Purpose:
            Signals provide a way to allow certain senders to notify a set of receivers when certain actions or events occur.
            They enable decoupled communication between different parts of a Django application or between different applications.
            
        Usage:
            You can use signals for handling events such as model instance creation (post_save),
             model instance deletion (post_delete), and other custom events.
            It allows you to execute specific code in response to events without directly coupling the sender and receiver.
    Middleware:
    
        Purpose:    
            Middleware is a way to process requests and responses globally before they reach the view or after they leave the view.
            It provides a hook-based architecture to process the request-response lifecycle.
        
        Usage:
            Middleware components can perform tasks such as authentication, logging, modifying the request or response, and more.
            They are executed in a specific order during the request-response cycle.
            
            
"""