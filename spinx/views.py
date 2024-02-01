from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from users.models import User
from .forms import  XstakeForm
from .models import Stake
from accounts.models import Account
    
def spinx(request,*args,**kwargs):    
    refercode = kwargs.get('refer_code')
    try:
        User.objects.get(code=refercode)
        if request.user.is_authenticated:
            logout(request)
        request.session['ref_code']=refercode
    except User.DoesNotExist:
        pass
    if not request.user.is_anonymous:    
        account = Account.objects.get(user=request.user)
        
   # if not request.user.is_anonymous:    
   #     trans_logz = Stake.objects.filter(
   #         account=account,
    #        ).order_by("-created_at")[:2]
    #else:
    #    trans_logz=[]

    if request.method == "POST":
        stake_form = XstakeForm(request.POST)
        if stake_form.is_valid():
            stake = stake_form.save(commit=False)
            stake.account = account#request.user
            stake.save()
            #return redirect('/')
    else:
        stake_form = XstakeForm()

    if not request.user.is_anonymous:
        spins = len(Stake.unspinnedx(request.user.id))                         

    else:
        spins=0 
        
    context = {
        "user": request.user,
        "stake_form": stake_form,
       # "trans_logz": trans_logz,
        "spins": spins,
    }
    return render(request, "spinx/ispinx.html", context)
    


@login_required(login_url="/user/login")
def stakes(request):
    account = Account.objects.get(user=request.user)
    trans_logz = Stake.objects.filter(
        account=account
    ).order_by("-created_at")[:20]


    context = {
        "trans_logz": trans_logz,
        }

    return render(request, "spinx/stakes.html", context)
