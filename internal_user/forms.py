from django import forms

class FundDepositForm(forms.Form):
    customerName = forms.CharField()
    customerId = forms.IntegerField()
    accountId = forms.IntegerField()
    accountType = forms.CharField()
    depositAmount = forms.FloatField()

class IssueChequeForm(forms.Form):
    customerName = forms.CharField()
    accountId = forms.IntegerField()
    accountType = forms.CharField()
    chequeAmount = forms.FloatField()
    recepientName = forms.CharField()

class CustomerForm(forms.Form):
    customerName = forms.CharField()
    customerId = forms.IntegerField()
    accountId = forms.IntegerField()
    accountType = forms.CharField()
    customerEmail = forms.EmailField()
    customerPhoneNum = forms.IntegerField()
