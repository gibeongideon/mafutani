#from celery import chain
from mpesa_api.core.tasks import (
    send_b2c_request_task,
    call_online_checkout_task,
    # process_b2c_call_response_task,
    # handle_online_checkout_response_task,
)

from django.dispatch import receiver
from mpesa_api.core.models import B2CRequest, OnlineCheckout
from django.db.models.signals import post_save


@receiver(post_save, sender=B2CRequest)
def handle_b2c_request_post_save(sender, instance, **kwargs):
    """
    Handles B2CRequest post_save
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """

    # call the mpesa
    send_b2c_request_task(
        int(instance.amount), instance.phone, instance.id
    ) 
    
    #process_b2c_call_response_task(instance.id)
    


@receiver(post_save, sender=OnlineCheckout)
def handle_online_checkout_post_save(sender, instance, **Kwargs):
    """
    Handle online checkout post save
    :param sender:
    :param instance:
    :param Kwargs:
    :return:
    """
    # online checkout
    call_online_checkout_task(
        instance.phone,
        int(instance.amount),
        instance.account_reference,
        instance.transaction_description,
        instance.is_paybill,
    )
    
    #handle_online_checkout_response_task(instance.id)
    


