from . import  views
from django.urls import path, include

app_name = "spix"

urlpatterns = [
    path("", views.spinx, name="spinx"),
    path("r/<str:refer_code>/", views.spinx, name="spinx"),    
    path("stakes", views.stakes, name="stakes"),
]
