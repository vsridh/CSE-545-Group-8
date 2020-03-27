from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from home import models

class ExtendedUserCreationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)

    class Meta:
        model=User
        fields=('username','email', 'first_name', 'last_name')

    def save(self):
        user = super().save(commit=False)
        user.username=self.cleaned_data['username']
        user.email=self.cleaned_data['email']
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields=('street_address', 'city', 'state', 'zip_code', 'mobile_number', 'birthdate', 'ssn',)

class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields=('account_type',)