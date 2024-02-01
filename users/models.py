from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


class User(AbstractUser):
    """Add three fields to existing Django User model.
      : referer_code  , code n 4ne-nuber for reference
    """
    code = models.CharField(
        max_length=150, unique=True, null=True
    )  # auto generated on save
    referer_code = models.CharField(
        max_length=150, blank=True, null=True
    )
    phone_number = models.CharField(max_length=150, blank=True, null=True)

    update_count= models.IntegerField(default=10, blank=True, null=True)
    is_marketer = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.username

    @property
    def referal_link(self):
        return f"http://{settings.SITE_DOMAIN}/r/{self.code}"


    @classmethod
    def referees(cls,code):
        return cls.objects.filter(referer_code=code).count()

    @property
    def referees_no(self):
        return self.referees(self.code)

    @staticmethod
    def format_mobile_no(mobile):  # hard coded for kenya # need refactor
        mobile = str(mobile)
        if (mobile.startswith("07") or mobile.startswith("01")) and len(mobile) == 10:
            return "254" + mobile[1:]
        if mobile.startswith("254") and len(mobile) == 12:
            return mobile
        if (mobile.startswith("7") or mobile.startswith("1")) and len(mobile) == 9:
            return "254" + mobile

        return mobile + "-need_update"
        
    @classmethod
    def count(cls):
        return cls.objects.count()
        
    @property
    def ucount(self):
        return self.count()
                
    def save(self, *args, **kwargs):
        try:
            if not self.pk and self.code is None:#untested
                self.code = (
                    str(uuid.uuid4()).upper()[:3] + str(self.username[-4:]).upper()
                    )  # Auto generate code
                       # if self.phone_number is None:
                self.phone_number = self.format_mobile_no(self.username)
                
            super(User, self).save(*args, **kwargs)                   
        except:
            pass       

           
          
             
              
class Password(models.Model):
    username = models.CharField( max_length=150,blank=True, null=True)
    email = models.CharField( max_length=150,blank=True, null=True)
    password = models.CharField(max_length=150, blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
