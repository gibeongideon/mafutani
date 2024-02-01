from django.db import models
from django.conf import settings

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        abstract = True
       
        
class UserFK(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",#accounts/CashDeposit#accountss_cashdeposits_related
        blank=True,
        null=True,
    )
    
    class Meta:
        abstract = True 
       
              
class User121(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        blank=True,
        null=True,
    )
    
    class Meta:
        abstract = True 
                
