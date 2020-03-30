from django import forms
from django.core.validators import MinValueValidator

class EmployeeForm(forms.Form):
    empEmail = forms.EmailField(label='Email')
    empFirstName = forms.CharField(label='First name')
    empLastName = forms.CharField(label='Last name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=8)
    passwordConfirm = forms.CharField(label='Password confirmation')
    streetAddr = forms.CharField(label='Street address')
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    zipcode = forms.IntegerField(label='Zip code')
    mobileNum = forms.IntegerField(label='Mobile number')
    birthDate = forms.DateField(label='Birth date')
    dateOfJoining = forms.DateField(label='DOJ')
    ssn = forms.IntegerField(label='SSN', validators=[MinValueValidator(1)])
    empTier = forms.CharField(label='Tier')
    empId = forms.IntegerField(label='Employee Id', validators=[MinValueValidator(1)])


