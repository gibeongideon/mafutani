from django.urls import path#, include
from . import  views

app_name = "rgames"

urlpatterns = [
    path("bets/", views.update_bets, name="update_bets"),
    path("sports/", views.sports, name="sports"),
]
