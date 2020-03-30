from django import forms

class LoginForm(forms.Form):
    user_id = forms.CharField(label='UserID', max_length=20)
    password = forms.CharField(max_length=15, widget=forms.PasswordInput)

class Otp(forms.Form):
    otp = forms.IntegerField()
    class Meta:
        fields=('otp',)

class Token(forms.Form):
    token = forms.IntegerField(widget=forms.HiddenInput())
    

