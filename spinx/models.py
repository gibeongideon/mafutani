from django.db import models
from django.conf import settings
from random import randint
from base.models import TimeStamp
from bet.models import BetRealTrial
from accounts.models import  Account,CentralBank
from django.contrib.auth import get_user_model
User = get_user_model()

        
class SpinxSetting(TimeStamp):
    refer_per = models.FloatField(default=5, blank=True, null=True)
    per_to_keep = models.FloatField(default=5, blank=True, null=True)
    min_bet = models.DecimalField(max_digits=5, default=4, decimal_places=2, blank=True, null=True)
    virtual_acc = models.FloatField(default=10000, blank=True, null=True)
    active = models.BooleanField(default=False,blank=True)

    class Meta:
        db_table = "spinx_settings"
        
def wheel_setting():
    set_up, created = SpinxSetting.objects.get_or_create(id=1)
    return set_up

class Stake(BetRealTrial):
    current_bal = models.FloatField(max_length=10, default=0,blank=True, null=True)  # R
    spinned = models.BooleanField(default=False, blank=True, null=True)
    win_multiplier = models.FloatField(max_length=10,default=0,blank=True, null=True)

    pointer = models.IntegerField(blank=True, null=True)
    closed = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"stake:{self.amount} by:{self.account}"

    @property
    def  min_stake(self):
        set_up=wheel_setting()
        return set_up.min_bet

    def bet_status(self):
         if self.spinned:
            return "spinned"
         else:
            return "pending"   
         
    @classmethod
    def unspinnedx(cls, account_id): 
        return [obj.id for obj in cls.objects.filter(account=account_id, spinned=False)]

    @property
    def active_spinsx(self):
        return self.unspinnedx(self.account.id)

    @property
    def expected_win_amount(self):
        if self.spinned:
           return "W="+str(self.win_multiplier*float(self.amount)) + ' (X'+ str(self.win_multiplier)+")"
        else:
           return  "B="+str(self.amount)  
             
    class Meta:
        db_table = "spinx_stakes"    
        
    @staticmethod
    def winner_selector(give_away,bet_amount):     
        wheel_map=settings.WHEEL_MAP  #WHEEL_MAP=[20,10,5,0,100,50,20,0,3,2,1,0,500,0,20,10,5,0,200,25,15,0,3,2,1,0,1000,0]
        chosen=[]
        for n in range(len(wheel_map)):
            val_at_n=wheel_map[n]
            if float(give_away)/float(bet_amount) >=float(val_at_n):
                chosen.append((n,val_at_n))   
                         
        return chosen[randint(0,len(chosen)-1)]              

    def update_reference_account(self,ref_credit):
        try:
            this_user = self.account.user
            this_user_refercode = (this_user.referer_code)  
            if not this_user.referer_code:
                this_user_refercode = User.objects.get(id=1).code  # settings       
            try:
                userr=User.objects.get(code=this_user_refercode)
            except User.DoesNotExist:
                userr=User.objects.get(id=1)
            referer_account = Account.objects.get(user=userr)

            if  this_user.is_marketer and userr.is_marketer:
                referer_account.add_tokens(ref_credit,trans_type="Ref-Com")  
            if  not this_user.is_marketer and not userr.is_marketer:
                referer_account.add_tokens(ref_credit,trans_type="Ref-Com") 
        except Exception as e:
            print(e)
             
    def update_giveaway_tokeep(self):
        set_up=wheel_setting()
        per_for_referer = set_up.refer_per        
        if per_for_referer > 100:
            per_for_referer = 0            
        ref_credit = (per_for_referer / 100) *  float(self.amount)         
        win_amount = float(self.amount) * self.win_multiplier
        
        if  self.account.user.is_marketer:
            give_away_bal=float(self.account.cbank.give_away_marketer)
            to_keep_bal=float(self.account.cbank.to_keep_marketer)
            field_away="GAM"
            field_to_keep="TKM"             
        else:
            give_away_bal=float(self.account.cbank.give_away)
            to_keep_bal=float(self.account.cbank.to_keep)
            field_away="GA"
            field_to_keep="TK"              
                                
        _to_keep=(float(set_up.per_to_keep) / 100) * float(self.amount) 
               
        if self.win_multiplier==0:            
            away = give_away_bal + float(self.amount) - _to_keep-ref_credit  
        else:
            away = give_away_bal - float(win_amount) - _to_keep - ref_credit+float(self.amount)
            self.account.add_tokens(float(win_amount),trans_type="rWIN")
   
        to_keep = to_keep_bal + _to_keep
        
        self.account.cbank.update_field(away,update_field=field_away)
        self.account.cbank.update_field(to_keep,update_field=field_to_keep) 
                  
        if ref_credit > 0:
           self.update_reference_account(ref_credit)
            
    def process_winner(self):
        amount=self.amount
        if self.real_account:
            if  self.account.user.is_marketer:
                current_bal = float(self.account.cbank.give_away_marketer)
            else:
                current_bal = float(self.account.cbank.give_away)
        else:#TRIAL-ACCOUNT
            set_up=wheel_setting()              
            current_bal = float(randint(0,set_up.virtual_acc))
             
        pointer,winner_multiplier = self.winner_selector(current_bal,amount) 
        self.pointer=pointer+1 #index_start_at_0       
        self.win_multiplier= winner_multiplier 
        if self.real_account:
            self.update_giveaway_tokeep()                
        else:
            self.account.add_tokens(float(winner_multiplier)*float(amount),trans_type="tWIN")
        self.closed = True    
        self.save() 
        return self
