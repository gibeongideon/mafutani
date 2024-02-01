from django.db import models
from datetime import datetime

def filter_html_elements(content):
    #TODO
    return content

class ContactSubject(models.Model):
    name =  models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = "d_contact_subjects"
        
    def __str__(self):
        return self.name
           
class ContactUs(models.Model):
    name =  models.CharField(max_length=100, blank=True, null=True)
    email =  models.CharField(max_length=100, blank=True, null=True)
    phone =  models.CharField(max_length=100, blank=True, null=True)    
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "d_contact_us"
        verbose_name_plural = "Contact Us Messages"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.message=filter_html_elements(self.message)#avoid XSS attack 
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)    
        
    def __str__(self):
        return self.name
   
   
class UserStat(models.Model):
    homepage_hits_login =  models.IntegerField(default=0, blank=True, null=True)
    homepage_hits_anonymous = models.IntegerField(default=0, blank=True, null=True)
    spinx_hits = models.IntegerField(default=0, blank=True, null=True)
    spinx_hits_anonymous = models.IntegerField(default=0, blank=True, null=True)
    #s_date=models.DateTimeField(default=datetime.now(), blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        db_table = "d_user_stat"
        get_latest_by ="id"
        
    def __str__(self):
        return "User Stats-"+str(self.id)
        
class FaqTopic(models.Model):
    name =  models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = "d_faqtopic"
        
    def __str__(self):
        return self.name
   
   
class FaqQa(models.Model):    
   # topic = models.ForeignKey(FaqTopic,on_delete=models.CASCADE,blank=True,null=True)
    question =  models.CharField(max_length=100, blank=True, null=True)
    answer = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "d_faqqa"
   
   
    def __str__(self):
        return self.question
   
        
    
class Info(models.Model):
    ref_mssg =  models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = "d_info"
        
    def __str__(self):
        return "INFO"