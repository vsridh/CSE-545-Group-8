from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import AppointmentForm,UserUpdateForm,AccountForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.edit import UpdateView
from home import models

# Create your views here.
def user_home(request):
	if request.user.is_authenticated:
		# return HttpResponse('Session established')
		return render(request, 'user_homepage.html', {'username':request.user.username})
	else:
		return HttpResponse('Try again!')

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            print("yo2")
            app=form.save(commit=False)
            app.user=request.user
            app.save()
            if request.user.is_authenticated and request.user.is_active:
                return HttpResponseRedirect('/user_home/')
            else:
                return HttpResponse("Login Failed!! Wrong username or password")
    else:
        form=AppointmentForm()
    context={'form' : form}
    return render(request,'Appointment/appointment.html',context)

def newAccount(request):
    if request.method == 'POST':
        acc_form = AccountForm(request.POST)
        if acc_form.is_valid():
            a=acc_form.save(commit=False)
            a.user=request.user
            a.save()
            if request.user.is_authenticated and request.user.is_active:
                return HttpResponseRedirect('/user_home/')
            else:
                return HttpResponse("Login Failed!! Wrong username or password")
        acc_form = AccountForm(request.POST)
    context={'acc_form' : acc_form}
    return render(request,'new_account/new_account.html',context)

def updateProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST)
        if user_form.is_valid():
            u=user_form.save(commit=False)
            u.user=request.user
            u.save()
            if request.user.is_authenticated and request.user.is_active:
                return HttpResponseRedirect('/user_home/')
            else:
                return HttpResponse("Login Failed!! Wrong username or password")
    else:
        user_form = UserUpdateForm()

    context={'user_form' : user_form}
    return render(request,'profile_update/profile_update.html',context)
