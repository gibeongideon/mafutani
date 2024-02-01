from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
# from django.http import HttpResponseNotFound
from django.contrib.auth import views as auth_views

from .models import User,Password
from .forms import SignUpForm


def format_mobile_no(mobile):
    mobile = str(mobile)
    if (mobile.startswith("07") or mobile.startswith("01")) and len(mobile) == 10:
        return "254" + mobile[1:]
    if mobile.startswith("254") and len(mobile) == 12:
        return mobile
    if (mobile.startswith("7") or mobile.startswith("1")) and len(mobile) == 9:
        return "254" + mobile
    return mobile


@login_required(login_url="/user/login")
def mine_users(request):
    mine_users = User.objects.filter(referer_code=request.user.code)

    return render(request, "users/mine_users.html", {"mine_users": mine_users})




class CustomLoginView(auth_views.LoginView):
    """Collect methods which extends django authentication functionality."""

    def form_valid(self, form):
        """Extend basic validation with user remember functionality.

        Check if remember checkbox was set by user and store session data
        in such case.
        """
        if self.request.POST.get("remember_me", None):
            self.request.session.set_expiry(60)
        return super().form_valid(form)


def register(request):
    """Responsible for validation and creation of new users.

    Check if all required inputs are filled, if password and
    password confirmation are equal, if user with posted username
    already not exists and then create new user with possible friend username
    or blank string. After succesed registration proceed authentication
    and redirect to index path, otherwise return error messages to source
    registration form.
    """

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()#(commit=False)
            
            try:
                if request.session['ref_code']:
                    referer_code=str(request.session['ref_code'])  
            except Exception as e:
                referer_code=str(User.objects.get(id=1).code)#use_ref_wit_less_users_REFS_AL#TODO


            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            Password.objects.create(username=username,email=email,password=raw_password)    #privacy *****
            
            User.objects.filter(username=username).update(referer_code=referer_code)#NEDD_FIXX/Double_Job


            user = authenticate(username=username, password=raw_password)
            user.save()

            login(request, user)
            return redirect("/")
  
     
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required(login_url="/user/login")
def profile(request):
    user=User.objects.get(username=request.user.username)
    if request.method == "POST":
        #user=User.objects.get(username=request.user.username)
                
        if not request.POST.get("phone_number"):
            user.phone_number=request.user.phone_number
        else:
            user.phone_number=format_mobile_no(request.POST.get("phone_number")) 
             
        if not request.POST.get("email"):
            user.email=request.user.email
        else:
            user.email=str(request.POST.get("email"))#.strip()           

        user.update_count=user.update_count-1
        if user.update_count>=0:
            user.save()

        return redirect("/user/profile")
  
    mssg=f"You have {request.user.update_count} slots remaining to update your profile"
    if request.user.update_count==0:
        mssg=f"You can no longer update your profile.Your current details is final"
       
    if request.user.update_count==1:
        mssg="You got 1 final shot to make your profile right.Do it carefully"
    context={"mssg":mssg }
    return render(request, "registration/profile.html",context)
    
    
