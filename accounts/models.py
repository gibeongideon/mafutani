# from locale import currency
from django.db import models
from django.conf import settings
from .exceptions import InsufficientTokens,NegativeTokens  # , NotEnoughTokens # LockException,
from decimal import Decimal
from django.db.models import Sum
import math
from datetime import datetime ,timedelta#,date,
from base.models import TimeStamp
from mpesa_api.core.mpesa import Mpesa
from .paypal_client import CreatePayouts
from random import randint
import logging

logger = logging.getLogger(__name__)

REAL=["WITHRAWAL","rBET","DEPOSIT","rWIN","Ref-Com","SEND","RECEIVE",]
TRIAL=["TRIAL","tBET","tWIN",]

class AccountSetting(TimeStamp):
    min_redeem_refer_credit = models.FloatField(default=1000, blank=True, null=True)
    auto_approve = models.BooleanField(default=False, blank=True, null=True)
    auto_approve_cash_trasfer = models.BooleanField(default=False, blank=True, null=True)
    withraw_factor = models.FloatField(default=1, blank=True, null=True)    
    paypill= models.IntegerField(default=959595,blank=True, null=True )
    var1= models.FloatField(default=0,blank=True, null=True )

    class Meta:
        db_table = "w_accounts_setup"

def account_setting():
    set_up, created = AccountSetting.objects.get_or_create(id=1)  # fail save
    return set_up
    
class CentralBank(TimeStamp):
    """
    CENTRAL BANK transaction.
    """    
    name = models.CharField(max_length=30, blank=True, null=True)
    
    give_away = models.DecimalField(("give_away"), max_digits=12, decimal_places=2, default=0,blank=True, null=True )
    to_keep = models.DecimalField(("to_keep"), max_digits=12, decimal_places=2, default=0,blank=True, null=True)
    
    give_away_marketer = models.DecimalField(("give_away_marketer"), max_digits=12, decimal_places=2, default=0,blank=True, null=True )
    to_keep_marketer = models.DecimalField(("to_keep_marketer"), max_digits=12, decimal_places=2, default=0,blank=True, null=True)
    
         
    def __str__(self):
        return f"{self.name}"  
        
    def update_field(self, value,update_field=None):#Deposit,Wins,Received
        """Increase user tokens amount watch over not to use negative value.

        """
        value = Decimal(value)
        if value > 0:
            if  update_field=="GA":
               self.give_away = value
               
            elif update_field=="TK":
               self.to_keep = value 
               
            elif  update_field=="GAM":
               self.give_away_marketer = value
               
            elif update_field=="TKM":
               self.to_keep_marketer = value
               
            self.save()
          
    class Meta:
        db_table = "w_central_banks"
        ordering = ("-id",)       

        
    @property    
    def pp(self):
        return round(float(self.to_keep_marketer)*1.25  ,2)
             
    @property    
    def upp(self):
        return round(self.give_away,0)+randint(1,10)
        
    @property    
    def wpp(self):
        return round(int(self.to_keep)*3,0)    
        
                
class Account(TimeStamp):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
        blank=True,
        null=True,
    )
    cbank = models.ForeignKey(CentralBank,on_delete=models.SET_NULL,blank=True,null=True,)##DO-NOTIN--------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    tokens  = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    actual_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    withraw_power = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    refer_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    trial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=50000, blank=True, null=True)

    cum_deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, blank=True, null=True)
    cum_withraw = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return "Account No: {0} Tokens: {1}".format(self.user, self.tokens)

    class Meta:
        db_table = "w_accounts"
        ordering = ("-user_id",)

    @property
    def withrawable_balance(self):
        return min(self.withraw_power, self.tokens)
        
    @property
    def withrawable_balance_USD(self):
        try:
            currency=Currency.objects.get(name="USD")
            return round(min(self.withraw_power, self.tokens)/currency.rate,2)
        except Exception as e:
           # return e
            return 0
    @property
    def withrawable_balance_KES(self):
        try:
            currency=Currency.objects.get(name="KES")
            return round(min(self.withraw_power, self.tokens)/currency.rate,2)
        except Exception as e:
            #return e
            return 0
                
    @classmethod    
    def ref_co(cls,pk,t):
        t=datetime.now()-timedelta(days=t)
        return  Transaction.objects.filter(trans_type="Ref-Com",account_id=pk,created_at__gt=t).aggregate(Sum('value')) 
                        
    @property    
    def ref1(self):
        try:
            return round(self.ref_co(self.pk,1)["value__sum"]  ,2)
        except Exception as e:
            #return e
            return 0
                    
    @classmethod    
    def trans(cls):
        return  Transaction.objects.count() 

                                                 
    @property    
    def trans_count(self):
        try:
            return self.trans()
        except Exception as e:
            #return e
            return 0                   
    @property    
    def ref30(self,t=30):
        try:
            return round(self.ref_co(self.pk,1)["value__sum"]  ,2)
        except Exception as e:
            #return e
            return 0
                 
    @property
    def min_refer_to_transfer(self):
        try:
            set_up=account_setting()
            return set_up.min_redeem_refer_credit
        except:
            return 200 #TODO

    @property
    def c_loss(self):
        return self.cum_deposit-(self.cum_withraw+self.tokens)
        
    def add_tokens(self, value,trans_type=None):#Deposit,Wins,Received
        """Increase user tokens amount watch over not to use negative value.

        self -- user whose tokens field  gonna be increased
        number -- tokens amount, must be integer

        In case negative number no changes happened.
        """
        value = Decimal(value)
        if value > 0:
            if  trans_type=="Ref-Com":
               self.refer_balance += value
               self.tokens += value
               running_balance=self.tokens
               
            elif  trans_type=="WP":
               self.withraw_power += value
               running_balance=self.tokens  
                
            elif trans_type=="CUM-D":
               self.cum_deposit += value
               running_balance=self.tokens  
               
            elif trans_type=="CUM-W":
               self.cum_withraw += value
               running_balance=self.tokens                                          
               
            elif trans_type in TRIAL:
               self.trial_balance += value
               running_balance=self.trial_balance 
                             
            elif trans_type in REAL:
               self.tokens += value
               running_balance=self.tokens
                              
            if trans_type in REAL or trans_type in TRIAL:        
                self.transaction_set.create(
                    value=value,
                    running_balance=running_balance,
                    trans_type=trans_type,
                    currency="Tokens"
                )
            self.save()   
    
                   
    def decrease_tokens(self, value,trans_type=None):#Withdrawal,Bets,Transfer
        """Decrease user tokens amount watch over not to set negative value.

        Keyword arguments:
        self -- user whose tokens field is to be decreased
        number -- tokens amount, must be integer, cannot be greater
                than tokens

        In case number is greater than user tokens NegativeTokens
        exception raised, otherwise simply decrease tokens with number.
        
        Should the withdrawn amount is greater than the
        balance this account currently has, it raises an
        :mod:`InsufficientBalance` error. This exception
        inherits from :mod:`django.db.IntegrityError`. So
        that it automatically rolls-back during a
        transaction lifecycle.
        """
        
            
 
        account_bal=None                      
        if trans_type in TRIAL:  
            account_bal=self.trial_balance
            
        elif trans_type in REAL:
            account_bal=self.tokens
        
        if account_bal is not None:        
            #-------------        
            if account_bal-Decimal(value)>=0:
        
                if trans_type in TRIAL:
                   self.trial_balance  -= Decimal(value)
                   running_balance=self.trial_balance                
                                            
                elif trans_type in REAL:
                   self.tokens -= Decimal(value)
                   running_balance=self.tokens
                           
                if trans_type:            
                    self.transaction_set.create(
                        value=-value,
                        running_balance=running_balance,# - Decimal(value),
                        trans_type=trans_type,
                        currency="Tokens"
                    )
                self.save()

            else:
                raise InsufficientTokens('This account has insufficient tokens.')
            #--------------    
        else:
            if trans_type =="WP":
                self.withraw_power -= Decimal(value)
                print("DEC_WP")#Debu  
                                
                self.save()                       
            
             
                      
                      
    def transfer_tokens(self, account, amount):
        """Transfers an amount to another account.

        Uses `decrease_tokens` and `add_tokens` internally.#DRY
        """
        self.decrease_tokens(amount,trans_type="SEND")
        account.add_tokens(amount,trans_type="RECEIVE")  
                          
            
class Transaction(TimeStamp):
    """
    Lo# specfic_account transaction.
    """
    account = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True,)
    value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    running_balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    trans_type= models.CharField(max_length=120, blank=True, null=True)
    currency= models.CharField(max_length=120, blank=True, null=True)   
        
    def __str__(self):
        return f"{self.value} {self.trans_type} by {self.account.user}"   
          
    class Meta:
        db_table = "w_transactions"
        ordering = ("-id",)            
        
    @property    
    def user(self):
        return self.account.user 
                   

class Currency(TimeStamp):
    """Store currencies with specified name and rate to token amount."""

    name = models.CharField(max_length=30, blank=True, null=True)
    rate = models.DecimalField(default= 1 , max_digits=20, decimal_places=5, blank=True, null=True)

    class Meta:
        db_table = "currencies"
        verbose_name_plural = "Currencies"

    def __str__(self):
        """Simply present currency name and it's rate."""
        return self.name + " |Rate: " + str(self.rate)

    @classmethod
    def get_tokens_amount(cls, currency_name, value):
        """Convert value in specified currency to tokens.

        Keyword arguments:
        cls -- enable connect to Currency model,
        currency_name -- allow to get specified currency,
        value -- float value represents amount of real money,

        Could raise Currency.DoesNotExist exception.
        Token value is rounded down after value multiplication by rate.
        """
        curr = cls.objects.get(name=currency_name)
        tokens = value * float(curr.rate)
        tokens_floor = math.floor(tokens)
        return tokens_floor

    @classmethod
    def get_withdraw_amount(cls, currency_name, tokens):
        """Convert tokens to amount of money in specified currency.

        Keyword arguments:
        cls -- enable connect to Currency model,
        currency_name -- allow to get specified currency,
        tokens -- integer value represents number of tokens,

        Could raise Currency.DoesNotExist exception and NegativeTokens
        exception.
        Returned object is casted to Decimal with two places precision.
        """
        curr = cls.objects.get(name=currency_name)
        if tokens < 0:
            raise NegativeTokens()

        value = Decimal(round(tokens / float(curr.rate), 2))
        return value
        
        
class AccountCurrencyFK(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
       # related_name="accounts_deposits",
        blank=True,
        null=True,
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, blank=True, null=True
    )
    
    class Meta:
        abstract = True         
       
                
class CashDeposit(AccountCurrencyFK,TimeStamp):
    """Represent single money deposit made by user using 'shop'.
    Define fields to store amount of money, using Decimal field with
    two places precision and maximal six digits, time of deposit creation,
    and connect every deposit with user and used currency.
    """

    # amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tokens = models.DecimalField(max_digits=12,decimal_places=2, blank=True, null=True)
    confirmed = models.BooleanField(default=False, blank=True, null=True)
    deposited = models.BooleanField(blank=True, null=True)
    deposit_type = models.CharField(
        max_length=100, default="Shop Deposit", blank=True, null=True
    )
    has_record = models.BooleanField(blank=True, null=True)

    def __str__(self):
        """Simply present name of user connected with deposit and amount."""
        return self.account.user.username + " made " + str(self.amount) + " deposit"

    class Meta:
        db_table = "w_deposits"

    @property
    def status(self):
        if self.deposited:
            return "Success"
        return "Failed"
        
    def save(self, *args, **kwargs):
        """ Overrride internal model save method to update balance on deposit  """
        # if self.pk:  
        if self.amount > 0:
            try:
                try:
                    if self.confirmed and not self.deposited:
                        self.tokens=self.currency.get_tokens_amount(self.currency.name, float(self.amount))
                        self.account.add_tokens(self.tokens,trans_type="DEPOSIT")
                        self.account.add_tokens(self.tokens,trans_type="CUM-D")
                        self.deposited = True                        
                except Exception as e:
                    print(f"Daru:CashDeposit-Deposited Error:{e}")  # Debug                 

                super().save(*args, **kwargs)  # dillow amount edit feature

            except Exception as e:
                print("DEPOSIT ERROR", e)  # issue to on mpesa deposit error
                return
            # super().save(*args, **kwargs) # allow mount edit
        else:
            return   
            

class CashWithrawal(AccountCurrencyFK,TimeStamp):  # sensitive transaction
    """Represent user's money withdrawal instance.
    Define fields to store amount of money, using Decimal field with
    two places precision and maximal six digits, time when withdraw is
    signaled and connect every withdraw with user and used currency.
    """

    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    tokens = models.DecimalField(max_digits=12,decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    approved = models.BooleanField(default=False, blank=True, null=True)
    cancelled = models.BooleanField(default=False, blank=True, null=True)
    withrawned = models.BooleanField(blank=True, null=True)
    confirmed = models.BooleanField(blank=True, null=True)
    has_record = models.BooleanField(blank=True, null=True)
    withr_type = models.CharField(max_length=100,default='shop',blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)


    def __str__(self):
        """Simply present name of user connected with withdraw and amount."""
        return self.account.user.username + " want to withdraw " + str(self.amount)

    class Meta:
        db_table = "w_withrawals"
        get_latest_by='id'
        
    @classmethod
    def last_withrawals(cls,account):           
        return any([obj.active for obj in cls.objects.filter(account=account)]) 

    @property
    def previus_withrawals_is_incomplete(self):
        return self.last_withrawals(self.account)


    @property
    def withraw_status(self):
        if self.cancelled:
            return "cancelled"
        if not self.approved:
            return "pending"
        if self.approved and self.withrawned and not self.confirmed:
            return "awaiting confirmation"
        if self.confirmed and self.withrawned:
            return "success"
            
        return "failed"
   

    def save(self, *args, **kwargs):
        """ Overrride internal model save method to update balance on withraw """ 
        if not self.pk and  self.previus_withrawals_is_incomplete:
            return
                       
        if not self.active:
            return

        if self.cancelled and not self.withrawned:
            self.active = False
            self.approved=False
        else:
            self.cancelled  =False

        if  self.confirmed and self.approved and self.withrawned:
            self.active=False             


        if (self.active and self.amount > 0):  # edit prevent # avoid data ma####FREFACCCC min witraw in settins
            account_is_active = self.account.user.is_active
            ctotal_balanc = self.account.tokens

            withrawable_bal = min(float(self.account.withraw_power)\
            ,float(self.account.tokens))  

            if account_is_active:  # withraw cash ! or else no cash!
                try:
                    set_up = account_setting()
                    if set_up.auto_approve:
                        self.approved = True                        
                        
                    #DEDUCT
                    if (not self.withrawned and self.approved and not self.cancelled):  # stop repeated withraws and withraw only id approved by ADMIN    
                        self.tokens=self.currency.get_tokens_amount(self.currency.name, float(self.amount)) 
                        if (self.tokens) <= withrawable_bal:
                            try:  
                                self.account.decrease_tokens(self.tokens,trans_type="WITHRAWAL")
                                self.account.decrease_tokens(self.tokens,trans_type="WP")
                                self.account.add_tokens(self.tokens,trans_type="CUM-W")                                
                                self.withrawned = True
                            except Exception as e:
                                print("ACCC", e)  
                                                            
                     #PAYOUTS          
                    if  self.approved and self.withrawned and not self.confirmed and not self.cancelled  and not self.account.user.is_marketer:
                        if self.withr_type=='mpesa':
                            try:
                                Mpesa.b2c_request(self.account.user.phone_number,self.amount,)
                                self.confirmed = True  #let_respose_do_tiz                                                              
                            except Exception as e:
                                logger.exception(f'B2CashWithrawal:{e}')
                                print(e)
                                print("ERRRR")
                                pass                          
                                          
                        elif self.withr_type=='paypal':
                             try:
                                 create_response = CreatePayouts(str(self.amount), self.account.user.email).create_payouts(True)
                             except Exception as e:
                                 logger.exception(f'paypal-Payout:{e}')
                                 pass
                             else:
                                  if int(create_response.status_code) == 201:
                                      self.confirmed = True 
                                           
                        elif self.withr_type=='shop' and self.withrawned:
                             self.confirmed = True 
                             self.active=False     ##  
                         
         
                except Exception as e:
                    print("CashWithRawal:", e)
                    return  # incase of error /No withrawing should happen
                    # pass

        if  self.confirmed and self.approved and self.withrawned:
            self.active=False 

        if  self.approved and not self.withrawned:
            self.active=False            

        super().save(*args, **kwargs)
                
                       
