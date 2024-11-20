# bancos/forms.py
from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, label="Deposit Amount")
    description = forms.CharField(max_length=255, required=False, label="Description", widget=forms.TextInput(attrs={'placeholder': 'Optional description'}))

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, label="Withdraw Amount")
    description = forms.CharField(max_length=255, required=False, label="Description", widget=forms.TextInput(attrs={'placeholder': 'Optional description'}))
