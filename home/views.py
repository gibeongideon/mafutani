from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import  ContactUsForm
from users.models import User
from .models import UserStat,FaqTopic,FaqQa
from accounts.models import  Transaction,Account,CentralBank
from  datetime import date
from django.core.paginator import Paginator
from home.models import Info

def contact(request): 
    mssg=""
    if request.method == "POST":
        
        cont_form = ContactUsForm(request.POST)
        #print(cont_form)
        if cont_form.is_valid():
            cont_form = cont_form.save(commit=False)
            
            if request.user.is_authenticated:
                cont_form.name = request.user.username 
                cont_form.email = request.user.email
                cont_form.save()
            mssg="Massage send!We will respond within 5 hours!"
            #return redirect('/contact-us')
            
    faqq=FaqQa.objects.all()
    #cont_form = ContactUsForm()
    
    context = {
        "user": request.user,
        "faqq":faqq,
        #"form":cont_form,
        "mssg": mssg,
    }
    
    return render(request, 'home/contact.html',context)


#def index(request):
 #   return render(request, 'home/index.html')


def index(request,*args,**kwargs):
    
    refercode = kwargs.get('refer_code')
    stat,_=CentralBank.objects.get_or_create(id=1)
    try:        
        User.objects.get(code=refercode)
        if request.user.is_authenticated:
            logout(request)
        request.session['ref_code']=refercode
    except User.DoesNotExist:
        pass     
    
    try:
       UserStat.objects.get(id=1)
    except:
       UserStat.objects.create(id=1)

    userstat=UserStat.objects.last()
      
    today=str(date.today())
    last_stat_date=str(userstat.created_at).split(" ")[0]

    if today!=last_stat_date:
       UserStat.objects.create()

    if not request.user.is_anonymous:       
        homepage_hits_login=userstat.homepage_hits_login+1
        userstat.homepage_hits_login=homepage_hits_login
        userstat.save()
    else:       
        homepage_hits_anonymous=userstat.homepage_hits_anonymous+1
        userstat.homepage_hits_anonymous=homepage_hits_anonymous
        userstat.save()

    faqq=FaqQa.objects.all()
    
    context = {
        "user": request.user,
        #"faqt":faqt,
        "faqq":faqq,
        "stat":stat,
    }

    return  render(request, 'home/index.html',context)
    


def affiliate(request):
    return render(request, 'home/affiliate.html')
        
def faqs(request):
    return render(request, 'home/faqs.html') 
   
          
@login_required(login_url="/user/login")    
def dashboard(request):
    wallet=Account.objects.get(user=request.user)
    trans=Transaction.objects.filter(account=wallet)
    paginator = Paginator(trans, 7) # Show 10 tras per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    info,_ =Info.objects.get_or_create(id=1)
        
        
            
    transr=trans[:5]
    mine_users = User.objects.filter(referer_code=request.user.code)
    context = {"user": request.user,"trans":trans,"transr":transr,"mine_users":mine_users,'page_obj': page_obj,"ref_mssg":info.ref_mssg}
    
    return render(request, 'home/dashboard.html',context)    
    
    
        
    
