from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("r/<str:refer_code>/", views.index, name="index"),
    path("contact-us", views.contact, name="contact"),
    path("affiliate", views.affiliate, name="affiliate"),
    path("faqs", views.faqs, name="faqs"),
    path("dashboard", views.dashboard, name="dashboard"),
    
]
