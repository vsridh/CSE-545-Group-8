from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from home import models

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields=('appointment_date','appointment_subject','appointment_assigned_to',)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = models.PendingProfileUpdate
        fields=('first_name', 'last_name','street_address','city','state','zip_code','mobile_number',)

class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields=('account_type',)


        