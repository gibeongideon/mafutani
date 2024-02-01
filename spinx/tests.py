from django.test import TestCase
from users.models import User
from spinx.models import (
    Stake,
    SpinxSetting,
)

from accounts.models import Account,CentralBank,Currency,CashDeposit
import random

def create_test_user(username,code, referer_code=None, is_marketer=False):
    """simplify create_test_user"""
    ran_value = random.randint(1000, 9999)
    email = f"user{ran_value}@winzan.com"
    return User.objects.create(username=str(username), email=email,code=str(code), referer_code=referer_code, is_marketer=is_marketer)

def deposit_to_test_user(account, amount=10000):
    currency=Currency.objects.create(name='KES',rate=1)    
    CashDeposit.objects.create(account=account, amount=amount, confirmed=True,currency_id=1)


class StakeTestCase(TestCase):
    def setUp(self):
        self.user = create_test_user("referer",code="REFERER",referer_code="REFEREE")
       # self.user.code="REFERER"
        self.user1= create_test_user("referee",code="REFEREE",referer_code="REFERER")
        
 
        self.userm = create_test_user("refererm",code="REFERERm",referer_code="REFEREEm", is_marketer=True)
        self.user1m= create_test_user("refereem",code="REFEREEm",referer_code="REFERERm", is_marketer=True)
                        
        self.currency=currency=Currency.objects.create(name='Tokens',rate=1)
        
        self.account=Account.objects.get(user=self.user)        
        self.account1=Account.objects.get(user=self.user1)
        
                
        self.accountm=Account.objects.get(user=self.userm)        
        self.account1m=Account.objects.get(user=self.user1m)
        
        deposit_to_test_user(self.account,amount=10000)
        deposit_to_test_user(self.accountm,amount=10000)
        
    def test_account_created(self):
        """
        Test :ACcount_Creation
        
        """        
        self.assertEqual(Account.objects.count(), 4)   
             
    def test_can_place_a_bet_wit_enough_balance_real_account(self):
        """
        Test :When real balance is available.User/Acount can place a bet successfully
        
        """        
        Stake.objects.create(real_account=True,account=self.account, amount=1000,currency=self.currency)
        Stake.objects.create(real_account=True,account=self.account, amount=1000,currency=self.currency)        

        self.assertEqual(Stake.objects.count(), 2)
        
    def test_can_not_place_a_bet_with_less_balance_real_account(self):
        """
        Test :When real balance is less.User/Acount CANNOT place a bet successfully
        
        """
        Stake.objects.create(real_account=True,account=self.account1, amount=10,currency=self.currency)
        Stake.objects.create(real_account=True,account=self.account1, amount=1000,currency=self.currency)        

        self.assertEqual(Stake.objects.count(), 0)

    def test_can_reduce_REAL_account_bal_on_bet(self):
        """
        Test :When real balance is less.User/Acount CANNOT place a bet successfully
        
        """
        Stake.objects.create(real_account=True,account=self.account, amount=1000,currency=self.currency)
        Stake.objects.create(real_account=True,account=self.account, amount=1000,currency=self.currency)        

        self.assertEqual(Stake.objects.count(), 2)  
        self.assertEqual(self.account.tokens,8000)
                      
        Stake.objects.create(real_account=True,account=self.account, amount=1000,currency=self.currency)
        Stake.objects.create(real_account=True,account=self.account, amount=1000,currency=self.currency)        
        
        self.assertEqual(Stake.objects.count(), 4)  
        self.assertEqual(self.account.tokens,6000)        
        
    def test_can_reduce_TRIAL_account_NOT_real_bal_on_bet(self):
        """
        Test :Can only reduce TRIAL BAL and Not Real Balance.ON Trial BET
        
        """
        Stake.objects.create(real_account=False,account=self.account, amount=1000,currency=self.currency)
        Stake.objects.create(real_account=False,account=self.account, amount=1000,currency=self.currency)        

        self.assertEqual(Stake.objects.count(), 2)  
        self.assertEqual(self.account.tokens,10000)
        self.assertEqual(self.account.trial_balance,48000.00)
                      
        Stake.objects.create(real_account=False,account=self.account, amount=1000,currency=self.currency)
        Stake.objects.create(real_account=False,account=self.account1, amount=1000,currency=self.currency)        
        
        self.assertEqual(Stake.objects.count(), 4)  
        self.assertEqual(self.account.tokens,10000)
        self.assertEqual(self.account.trial_balance,47000.00)
        self.assertEqual(self.account1.trial_balance,49000.00)
        self.assertEqual(self.account1.tokens,0)
        
        
    def test_centralBank_auto_create_on_user_creation(self):
        """
        Test :CentralBank is suppose to be created auto
        
        """
        self.assertEqual(CentralBank.objects.count(), 1)        
        
    def test_initial_CentralBank_correctness(self):
        """
        Test :CentralBank is suppose to be created auto
        
        """
        cb=CentralBank.objects.get(id=1)
        self.assertEqual(cb.give_away, 0)        
        self.assertEqual(cb.to_keep, 0)
        self.assertEqual(cb.give_away_marketer, 0)
        self.assertEqual(cb.to_keep_marketer, 0)
        
    def test_initial_CentralBank_On_OutCo(self):
        """
        Test :initial_CentralBank_On_OutCo
        
        """
        cb=CentralBank.objects.get(id=1)
        
        sk=Stake.objects.create(real_account=True,account=self.account, amount=1000,currency=self.currency)
        ou=Stake.objects.get(id=sk.id).process_winner()       
        self.assertEqual(Stake.objects.count(), 1)        
             
        self.assertEqual(cb.give_away, 0)        
        self.assertEqual(cb.to_keep, 0)
        self.assertEqual(cb.give_away_marketer, 0)
        self.assertEqual(cb.to_keep_marketer, 0) 
               
        
    def test_CB_CORRECT(self):
        """
        Test :initial_CentralBank_On_OutCo-CRITICAL_TEST        
        """
        cb=CentralBank.objects.get(id=1)
        cb.give_away=10000
        cb.save()

        ab=self.account.tokens
        sk=Stake.objects.create(real_account=True,account=self.account, amount=100,currency=self.currency)
        af=self.account.tokens
        
        ou=Stake.objects.get(id=sk.id).process_winner()  
        self.assertEqual(Stake.objects.count(), 1)
        win=ou.win_multiplier*ou.amount
        
        if win==0:
            self.assertEqual(self.account.tokens,af+win)
            ded=sk.amount
        else:
            self.assertEqual(self.account.tokens,af+win)  
            ded=win - sk.amount
            ded=-ded
        
        per=SpinxSetting.objects.get(id=1)
        rfp=per.refer_per
        tkp=per.per_to_keep
        
        
        rf=rfp/100*sk.amount
        tk=tkp/100*sk.amount        
        tt=rf+tk
                       
        self.assertEqual(CentralBank.objects.get(id=1).give_away,ded-tt)        
        self.assertEqual(CentralBank.objects.get(id=1).to_keep, tk)
        self.assertEqual(CentralBank.objects.get(id=1).give_away_marketer, 0)
        self.assertEqual(CentralBank.objects.get(id=1).to_keep_marketer, 0) 
        
        #__________________________________________________________________________________________________________________
        
        cb=CentralBank.objects.get(id=1)


        ab=self.account.tokens
        sk=Stake.objects.create(real_account=True,account=self.accountm, amount=200,currency=self.currency)
        af=self.accountm.tokens
        
        ou=Stake.objects.get(id=sk.id).process_winner()  
        self.assertEqual(Stake.objects.count(), 2)
        win=ou.win_multiplier*ou.amount
        
        if win==0:
            self.assertEqual(self.accountm.tokens,af+win)
            ded2=sk.amount
        else:
            self.assertEqual(self.accountm.tokens,af+win)  
            ded2=win- sk.amount
            ded2=-ded2
        
        per=SpinxSetting.objects.get(id=1)
        rfp=per.refer_per
        tkp=per.per_to_keep
        
        
        rf2=rfp/100*sk.amount
        tk2=tkp/100*sk.amount        
        tt2=rf2+tk2
       
                
        self.assertEqual(CentralBank.objects.get(id=1).give_away,ded-tt)        
        self.assertEqual(CentralBank.objects.get(id=1).to_keep, tk)
        self.assertEqual(CentralBank.objects.get(id=1).give_away_marketer, ded2-tt2)
        self.assertEqual(CentralBank.objects.get(id=1).to_keep_marketer, tk2) 
        
        #__________________________________________________________________________________________________________________        
                
        cb=CentralBank.objects.get(id=1)                      
                
        ab=self.account.trial_balance
        sk=Stake.objects.create(real_account=False,account=self.account, amount=100,currency=self.currency)
        af=self.account.trial_balance
                
        Stake.objects.get(id=sk.id).process_winner()  
        self.assertEqual(Stake.objects.count(), 3)
             
        win=sk.win_multiplier*sk.amount 
                
        self.assertEqual(self.account.trial_balance,af+win)
        
                
        self.assertEqual(CentralBank.objects.get(id=1).give_away,ded-tt)        
        self.assertEqual(CentralBank.objects.get(id=1).to_keep, tk)
        self.assertEqual(CentralBank.objects.get(id=1).give_away_marketer, ded2-tt2)
        self.assertEqual(CentralBank.objects.get(id=1).to_keep_marketer, tk2)
        
        
