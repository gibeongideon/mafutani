from django.shortcuts import render#, redirect, reverse
#from django.contrib.auth.decorators import login_required
from .models import Bet
import datetime
try:
    from account.models import (
    current_account_bal_of,
    update_account_bal_of,
    )    
except ImportError:
    pass  
    

from django.views.decorators.cache import cache_page
from .util import gamesapi

def latest_entry(request, blog_id):
    return datetime.datetime.now#Entry.objects.filter(blog=blog_id).latest("published").published


def sports(request):
   
    context=gamesapi.get_games()
    
  
        
    print(context)
    print("CONTEXT")
     
    return render(
        request,
        "rgames/sports.html",context
    )

#ascy
@cache_page(60 * 15)
#@condition(last_modified_func=latest_entry)
def games(request):
    return render(
        request,
        "rgames/games.html",
        {
            "games": gamesapi.get_games(),

        },
    )

    
#@cache 10 inute/api request here
def placebet(request):
    """
    API place bet using payload/Kinda FrontEnd betSpip/Cart_ecommerce
    payload={
    
    "marketCode":34534,
    "odds":1.76
    
    
    }
    """
    #TODO
    pass
    
def bets(request):#get all bet for user
    """filter active bets and update/save if #status is not None
    #then display
    #link to Stake details/add remove feature@@@IMP
    """
    #TODO
    pass 


#@login_required(login_url="/user/login")
def update_bets(request):
    active_bets = Bet.objects.filter(user=request.user,active=True)#.order_by("-id")[:10]
    if active_bets:
        for bet in active_bets:
            if bet.status is not None:
                if bet.status:
                    current_bal = current_account_bal_of(request.user)  # F1
                    new_bal = current_bal + bet.possiple_win_amount 
                    update_account_bal_of(request.user, new_bal)  # #F3
                    bet.active=False
                    bet.save()
                 #else:
                 
                    # pass
                     #referal_add
                                            
    return render(
        request,
        "rgames/update_bets.html",
        {
            "bets": active_bets,

        },
    )

