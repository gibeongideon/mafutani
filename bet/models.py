from django.db import models
from base.models import TimeStamp,UserFK
from accounts.models import AccountCurrencyFK
  
class BaseBet(AccountCurrencyFK,TimeStamp):
    amount = models.DecimalField(
        ("amount"), max_digits=12, decimal_places=2, default=50
    )       
                
    class Meta:
        abstract = True            
               
class BetRealTrial(BaseBet):
    real_account = models.BooleanField(default=False)
    placed = models.BooleanField(default=False)

    def account_type(self):
        if self.real_account:
            return "REAL"
        return "TRIAL" 
  
    def save(self, *args, **kwargs): 
        if not self.placed and self.amount >= 1:
            tokens=self.currency.get_tokens_amount(self.currency.name,float(self.amount))
            try:
                if self.real_account:
                    self.account.decrease_tokens(tokens,trans_type="rBET")
                    self.account.add_tokens(tokens,trans_type="WP")
                    self.placed=True
                else:
                    self.account.decrease_tokens(tokens,trans_type="tBET")
                    self.placed=True
                    
                #super().save(*args, **kwargs)
            except Exception as e:#InsufficientTokens
               # print(e)
                return
                
        super().save(*args, **kwargs)
                
    class Meta:
        abstract = True      

