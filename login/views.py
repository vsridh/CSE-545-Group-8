from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from datetime import datetime
from create_account import forms
from home.models import User,Profile
from .forms import LoginForm,Otp,Token
import time
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.encoding import force_text
from random import randint
from django.urls import reverse


#try wrong account list ------ username: number of try
block_wait_list={}
#blcok list -------username: start time
block_list={}


def login_user(request):
    global block_wait_list
    global block_list
    try_times=0
    if request.method=='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            userObj = authenticate(username=form.cleaned_data['user_id'], password=form.cleaned_data['password'])
            request.session['username'] = form.cleaned_data['user_id']
            request.session['password'] = form.cleaned_data['password']
            user_instance=User.objects.get(username=form.cleaned_data['user_id'])
            profile_instance=Profile.objects.get(user=user_instance)
            #check block list
            if form.cleaned_data['user_id'] in block_list:
                #check block time
                start_time=block_list[form.cleaned_data['user_id']]
                end_time=time.time()
                if ((start_time != 0) & (end_time - start_time <= 600)):
                    #return to block page
                    return login_block(request)

            #login#delete user in block list
                if form.cleaned_data['user_id'] in block_list:
                    block_list.pop(form.cleaned_data['user_id'])
                if form.cleaned_data['user_id'] in block_wait_list:
                    block_wait_list.pop(form.cleaned_data['user_id'])
                #return user home page
            elif userObj is None or profile_instance.flag==False or user_instance.is_active==False:
                #not in block list add
                if form.cleaned_data['user_id'] in block_wait_list:
                    try_times=block_wait_list[form.cleaned_data['user_id']]
                    block_wait_list[form.cleaned_data['user_id']] = try_times + 1
                else:
                    block_wait_list[form.cleaned_data['user_id']] = 1
                #check try times
                #start block
                if(try_times>=3):
                    #add block time
                    start_time=time.time()
                    block_list[form.cleaned_data['user_id']]=start_time
                    block_wait_list.pop(form.cleaned_data['user_id'])
                    return login_block(request)
            #if authorization is successful, redirect to appropriate page
            #return HttpResponseRedirect('/')
            elif userObj is not None and profile_instance.flag==True and user_instance.is_active:
                token=randint(10000,99999)
                to_email=user_instance.email
                mail_subject = 'Login OTP'
                message = render_to_string('authenticate_otp.html', {
                'user': request.user,
                'otp' : token
                 })
                email = EmailMessage(
                            mail_subject,message, to=[to_email]
                )
                email.send()
                request.method='GET'
                request.session['token'] = token
                return verify_otp(request)
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form':form})

def login_block(request):
    return HttpResponse("Login block!!need wait for")

def verify_otp(request):
    if request.method == 'POST':
        form = Otp(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            if form.cleaned_data['otp'] == request.session['token']:
                userObj = authenticate(username=request.session['username'], password=request.session['password'])
                login(request,userObj)
                request.session['last_activity'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                return HttpResponseRedirect('http://127.0.0.1:8000/user_home')
        return HttpResponse("Login Failed!! Wrong OTP")
    else:
        form = Otp()
    context={'form' : form}
    return render(request,'enter_otp.html',context)




