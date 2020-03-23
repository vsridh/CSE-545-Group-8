from django import forms

class FundDepositForm(forms.Form):
    customerName = forms.CharField()
    customerId = forms.IntegerField()
    accountId = forms.IntegerField()
    accountType = forms.CharField()
    depositAmount = forms.FloatField()