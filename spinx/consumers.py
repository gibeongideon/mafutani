import json
from channels.generic.websocket import WebsocketConsumer
from .models import  Stake,SpinxSetting
from accounts.models import Account,Currency

def account_setting():
    set_up, created = SpinxSetting.objects.get_or_create(id=1)  # fail save
    return set_up
    
class XspinConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.account=Account.objects.get(user=self.user)
        self.currency,_=Currency.objects.get_or_create(name="Tokens")
        self.accept()

    def disconnect(self, close_code):
        pass

    def update_stake_as_spinned(self, stakeid):
        Stake.objects.filter(currency=self.currency,account=self.account, id=stakeid).update(spinned=True)
               
    def place_bet(self,amount,real_account):
        amount=int(amount)        
        Stake.objects.create(currency=self.currency,account=self.account,amount=amount,real_account=real_account)   
        return amount
            
    def return_pointer(self):
        spinz = Stake.unspinnedx(self.account)
        if len(spinz) > 0:
            spin_id = spinz[0]
            self.update_stake_as_spinned(spin_id)
            pointer_obj= Stake.objects.get(id=spin_id).process_winner()            
            win_a=float(pointer_obj.win_multiplier*float(pointer_obj.amount))
            return pointer_obj.pointer,win_a
        else:
            return 888,None

    # Receive pointer from spin group
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        ipointer = text_data_json["ipointer"]
        message = text_data_json['message']
        real_cash = text_data_json['real_cash']
        
        if message =="None":
            ipointer,win_a = self.return_pointer()
            self.send(text_data=json.dumps({"ipointer": ipointer,"win_a": win_a,}))
        else:
            try:
                amount=int(message)
                
                if real_cash is True:
                   bal=int(self.account.tokens)
                   real_cash=True
                else:
                   bal=int(self.account.trial_balance)
                   real_cash=False

                setup=account_setting()                                       
         
                if bal>=amount:
                    if  amount  >= setup.min_bet:
                        bet=self.place_bet(amount,real_cash)
                        bet_s='BET'
                    else:
                        bet_s = 'MM'
                        bet = int(setup.min_bet)
                else:
                    bet_s ='NC' 
                    bet=0 
                                                  
                self.send(text_data=json.dumps({"bet": bet,"bet_s": bet_s,"bal": bal,}))
            except Exception as ce:
                pass
                print('NO_INTTT',ce)
