from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm

def login_user(request):
    if request.method=='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            userObj = authenticate(username=form.cleaned_data['user_id'], password=form.cleaned_data['password'])
            if userObj is not None:
                login(request,userObj)                
                return HttpResponseRedirect('/user_home/')
            else:
                return HttpResponse("Login Failed!!")
            #if authorization is successful, redirect to appropriate page
            #return HttpResponseRedirect('/')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form':form})

