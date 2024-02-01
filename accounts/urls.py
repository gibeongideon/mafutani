from django.urls import path, include
from . import paypalviews as ppviews
from . import mpesa_views as mviews
from . import views

app_name = "accounts"

urlpatterns = [
    path('paypal/checkout/', ppviews.checkout, name='paypal-checkout'),
    path('paypal/process-payment/', ppviews.process_payment, name='process_payment'),
    path('paypal/payment-done/', ppviews.payment_done, name='payment_done'),
    path('paypal/payment-cancelled/', ppviews.payment_canceled, name='payment_cancelled'),
    path("paypal/withrawal/", ppviews.paypal_withrawal, name="paypal_withrawal"),
    
    path("mpesa/deposit/", mviews.mpesa_deposit, name="mpesa_deposit"),
    path("mpesa/withrawal/", mviews.mpesa_withrawal, name="mpesa_withrawal"),
    path("all_withrawal/", views.all_withrawal, name="all_withrawal"),
   
]
