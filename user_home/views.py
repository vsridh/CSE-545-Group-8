from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_home(request):
    if request.user.is_authenticated:
        return render(request, 'summary.html', {"title": "Summary", "username": "User"})
    else:
        return HttpResponse('Try again!')


def user_accounts(request):
    if request.user.is_authenticated:
        return render(request, 'accounts.html', {"title": "Accounts", "username": "User"})
    else:
        return HttpResponse('Try again!')
