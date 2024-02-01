from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required



from .models import  CashWithrawal, Account
from users.models import User



@login_required(login_url="/user/login")
def all_withrawal(request):
    account = Account.objects.get(user=request.user)
    trans_logz = CashWithrawal.objects.filter(account=account).order_by("-id")[:20]
    context={"trans_logz": trans_logz,}
       
    return render(
        request,
        "accounts/all_withrawal.html",
        context
   )


 


