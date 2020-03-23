from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from datetime import datetime

from .forms import LoginForm
import time

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

            #check block list
            if form.cleaned_data['user_id'] in block_list:
                #check block time
                start_time=block_list[form.cleaned_data['user_id']]
                end_time=time.time()
                if ((start_time != 0) & (end_time - start_time <= 600)):
                    #return to block page
                    return login_block(request)

            #login
            if userObj is not None:
                login(request,userObj)     
                request.session['last_activity'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

                #delete user in block list
                if form.cleaned_data['user_id'] in block_list:
                    block_list.pop(form.cleaned_data['user_id'])

                #return user home page
                return HttpResponseRedirect('/user_home/')
            else:
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
                    return login_block(request)

                return HttpResponse("Login Failed!! Wrong username or password"+str(try_times+1))
            #if authorization is successful, redirect to appropriate page
            #return HttpResponseRedirect('/')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form':form})

def login_block(request):
    return HttpResponse("Login block!!need wait for")



