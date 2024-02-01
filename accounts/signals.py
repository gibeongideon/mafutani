from unicodedata import name
from .models import (
    Account,
    CentralBank,
    CashDeposit,
    CashWithrawal
)
from .models import account_setting,Currency
from mpesa_api.core.models import OnlineCheckoutResponse,B2CResponse

from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        bank,created=CentralBank.objects.get_or_create(name="CB")
        Account.objects.update_or_create(user=instance,cbank=bank)


@receiver(post_save, sender=OnlineCheckoutResponse) 
def update_account_balance_on_mpesa_deposit(sender, instance, created, **kwargs):
    # if created:
    try:
        successful_and_not_duplicate_response=int(instance.result_code) == 0 and len(OnlineCheckoutResponse.objects.filter(mpesa_receipt_number=instance.mpesa_receipt_number))==1
        if successful_and_not_duplicate_response:#make deposit
            try:
                this_user = User.objects.get(phone_number=str(instance.phone))
            except User.DoesNotExist:
                this_user = User.objects.create_user(
                    username=str(instance.phone), password=str(instance.phone)
                )  # 3#??
                
            try:
                currency=Currency.objects.get(name='KSH')  
            except Currency.DoesNotExist: 
                Currency.objects.create(name="KSH",rate=1) 
                currency=Currency.objects.get(name='KSH')

            CashDeposit.objects.create(
                account=Account.objects.get(user=this_user),
                amount=instance.amount,
                deposit_type="m-pesa",
                currency=currency,
                confirmed=True,
            )
        else:
            pass

    except Exception as e:
        print("MPESA DEPO", e)


@receiver(post_save, sender=B2CResponse) 
def update_cashwithrawal_on_mpesa_withrawal(sender, instance, created, **kwargs):
    pass

        

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.
        try:
            my_pk = int(ipn_obj.invoice)
            mytransaction = CashDeposit.objects.get(pk=my_pk)
            assert ipn_obj.mc_gross == mytransaction.amount and ipn_obj.mc_currency == 'USD'
        except Exception:
            logger.exception('Paypal ipn_obj data not valid!')
        else:
            logger.exception('Confirmed Completed Paypal Deposit Transaction!')
            mytransaction.confirmed = True
            mytransaction.save()
       
    else:
        logger.debug('Paypal payment status not completed: %s' % ipn_obj.payment_status)


valid_ipn_received.connect(paypal_payment_received)

