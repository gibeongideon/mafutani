from django import forms
from .models import CashWithrawal#, RefCreditTransfer, CashTransfer

class CashWithrawalForm(forms.ModelForm):
    class Meta:
        model = CashWithrawal
        fields = (
            "account",
            "amount",
            "withr_type",
            "currency",
        )


#class ReferTranferForm(forms.ModelForm):
#    class Meta:
#        model = RefCreditTransfer
#        fields = (
#            "user",
#            "amount",
#        )

#class CashTransferForm(forms.ModelForm):
#    class Meta:
#        model = CashTransfer
#        fields = (
#            "sender",
#            "recipient",
#            "amount",
 #       )
