from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import ExtendedUserCreationForm, UserProfileForm, AccountForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from home.models import Privilege

def homepage(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        account_form =AccountForm(request.POST)
        if form.is_valid() and profile_form.is_valid() and account_form.is_valid():
            user= form.save()
            acc=account_form.save(commit=False)
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.privilege_id=Privilege.objects.get(user_type="Customer")
            acc.user=profile.user
            profile.save()
            acc.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            return HttpResponseRedirect('/login/')
    else:
        form=ExtendedUserCreationForm()
        profile_form=UserProfileForm()
        account_form=AccountForm()

    context={'form' : form, 'profile_form' : profile_form, 'account_form' : account_form}
    return render(request,'create_account/register.html',context)
# Create your views here.