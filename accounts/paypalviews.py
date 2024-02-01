from paypal.standard.forms import PayPalPaymentsForm
from django.conf import  settings
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from django.conf import settings

from .models import (
    CashWithrawal,
    Account,
    AccountSetting,
    CashDeposit,
    Currency
)
from .forms import CashWithrawalForm
    
@login_required(login_url="/user/login")
def process_payment(request):
    amount = float(request.session['paypal_deposit_amount'])
    #host =settings.SITE_DOMAIN  # 
    host = request.get_host()
    try:
        currency=Currency.objects.get(name="USD")
    except Currency.DoesNotExist:
        Currency.objects.create(name="USD",rate=100) 
        currency=Currency.objects.get(name="USD")

    try:
        dlatest=CashDeposit.objects.filter(account=Account.objects.get(user=request.user)).latest('id')
        if dlatest.amount== amount:
            depo=dlatest
        else:
            depo=CashDeposit.objects.create(
                account=Account.objects.get(user=request.user),
                amount=amount,
                currency=currency,
                deposit_type="Paypal",)
    except:
        depo=CashDeposit.objects.create(
            account=Account.objects.get(user=request.user),
            amount=amount,
            currency=currency,
            deposit_type="Paypal",)                   


    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f'{amount}',
        'item_name': 'Winzangu-Deposit',
        'invoice': f'{depo.id}',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}/'.format(host),
        'cancel_return': 'http://{}/accounts/paypal/checkout'.format(host),
  
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(
        request,
        'accounts/paypal/process_payment.html',
        {'amount': amount, 'form': form})


def checkout(request):
    if request.method == 'POST':
        request.session['paypal_deposit_amount']=request.POST.get("amount")
        return redirect('/accounts/paypal/process-payment')
    else:
        return render(request, 'accounts/paypal/checkout.html')


@csrf_exempt
def payment_done(request):
    return render(request, 'accounts/paypal/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'accounts/paypal/payment_cancelled.html')




@login_required(login_url="/user/login")
def paypal_withrawal(request):
    uf = Account.objects.get(user=request.user)
    try:
        currency=Currency.objects.get(name="USD")
    except Currency.DoesNotExist:
        Currency.objects.create(name="USD",rate=100) ###
        currency=Currency.objects.get(name="USD")


    form = CashWithrawalForm()
    if request.method == "POST":
        data = {}
        data["account"] = uf
        data["amount"] = request.POST.get("amount")
        data["withr_type"] = 'paypal'
        data["currency"] = currency
        form = CashWithrawalForm(data=data)
        if form.is_valid():
            form.save()
            return redirect("/accounts/all_withrawal")#
       
    #trans_logz = CashWithrawal.objects.filter(user=request.user,withr_type='paypal').order_by("-id")[:10]

    return render(
        request,
        "accounts/paypal_withrawal.html",
        {"form": form,},
        
       # {"form": form, "trans_logz": trans_logz,"uf": uf},
    )

