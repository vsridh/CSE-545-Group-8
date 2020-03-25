from django import forms
from django.core.validators import MinValueValidator

class FundDepositForm(forms.Form):
    customerName = forms.CharField()
    customerId = forms.IntegerField(validators=[MinValueValidator(1)])
    accountId = forms.IntegerField(validators=[MinValueValidator(1)])
    accountType = forms.CharField()
    depositAmount = forms.FloatField(validators=[MinValueValidator(0.01)])

class IssueChequeForm(forms.Form):
    customerName = forms.CharField()
    accountId = forms.IntegerField(validators=[MinValueValidator(1)])
    accountType = forms.CharField()
    chequeAmount = forms.FloatField(validators=[MinValueValidator(0.01)])
    recepientName = forms.CharField()

class CustomerForm(forms.Form):
    customerName = forms.CharField()
    customerId = forms.IntegerField(validators=[MinValueValidator(1)])
    accountId = forms.IntegerField(validators=[MinValueValidator(1)])
    accountType = forms.CharField()
    customerEmail = forms.EmailField()
    customerPhoneNum = forms.IntegerField(validators=[MinValueValidator(1)])
