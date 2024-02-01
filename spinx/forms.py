from django import forms
from .models import Stake

class XstakeForm(forms.ModelForm):
    class Meta:
        model = Stake
        fields = ("account", "amount", "real_account")        
