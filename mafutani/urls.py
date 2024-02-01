"""mafutani URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("spinx.urls", namespace="spinx")),
    path('home', include('home.urls')),
    path("user/", include("users.urls", namespace="users")),
    path('rgames/', include('rgames.urls')),
    path('accounts/', include('accounts.urls')),
    # path("spinx/", include("spinx.urls", namespace="spinx")),
    path(settings.SECRET_MPESA_URL +"/pesa/", include("mpesa_api.core.urls", "mpesa")),#avoid fake callback by hackers
    path('paypal/', include('paypal.standard.ipn.urls')), 
    
]
