from django.db import models
from users.models import User
from base.models import TimeStamp
from bet.models import BaseBet
    
#FrontEnd_Payload
# payload =[(3456,""),(5432,""),(3455,"")]+amount

class Market(TimeStamp):
    code= models.CharField(max_length=1000,blank=True, null=True)#primary
    odds = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    result= models.BooleanField(blank=True, null=True)#W or L

    def __str__(self):
        return 'MKT:'+str(self.code)
        
class Bet(BaseBet):
    """
    Instant of Bet by User/Can have one or many markets
    """

    bet_slip = models.ForeignKey(
        'BetSlip',
        on_delete=models.CASCADE,
        related_name="bet_slips",
        blank=True,
        null=True,
    )          

    active= models.BooleanField(default=True, blank=True, null=True)#W or L
    
    def __str__(self):
        return "Bet "+str(self.id)+"by "+str(self.account)+':'+str(self.amount)
        

   ##OUTSITE/IN_IEW
    def update_account_on_win(self):      
        #TODO
        self.active=False
        pass
        ##OUTSITE/IN_IEW
    def update_account_on_lose(self):      
        #TODO
        self.active=False
        pass

                 
    def save(self, *args, **kwargs): 
        if not self.pk:
            tokens=self.currency.get_tokens_amount(self.currency.name,float(self.amount))
            try:
                self.account.decrease_tokens(tokens,trans_type="rBET")
                super().save(*args, **kwargs)
            except Exception as e:
                print(e)
                return      
        
    

class BetSlip(TimeStamp):
    """
    Instant of general betslip that can be used by many users
    """
    market = models.ManyToManyField(
        Market,
        #on_delete=models.CASCADE,
        related_name="marketss",
        blank=True,
        #null=True,
    )#JSONFIELD#NO
    def __str__(self):
        return str(self.id)
