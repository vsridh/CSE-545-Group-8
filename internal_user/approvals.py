from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from home.models import Privilege
from home.models import Profile
from home.models import Account
from django.contrib.auth.models import User


def getUnapprovedProfiles():
    unapproved_profiles = Profile.objects.filter(flag=False)
    profile_list = []
    #convert from 'QuerySet' to normal Python list
    for p in unapproved_profiles:
        profile_list.append(p)
    return profile_list

def getCriticalTransactions():
    #TO BE IMPLEMENTED
    return []

def _viewRequests(request):
    '''
    check logged in
    check user type
    determine type of requests to be shown
    get requests from db
    create context variable
    render page
    '''
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    context = {}

    if request.user.Profile_User.privilege_id.user_type == settings.SB_USER_TYPE_TIER_1 or request.user.Profile_User.privilege_id.user_type == settings.SB_USER_TYPE_TIER_2:
        profile_list = getUnapprovedProfiles()
        context['unapproved_profiles'] = profile_list
        '''
    elif request.user.profile.user_type == settings.SB_USER_TYPE_TIER_2:
        critical_transactions = getCriticalTransactions()
        context['critical_transactions'] = critical_transactions
        '''
    else:
        return HttpResponse("<h1>Error: 403 Forbidden</h1>")

    return render(request, 'pendingTransactions.html', context)


def handleUserRegistrationApproval(request):
    
    if not request.user.Profile_User.privilege_id.user_type == settings.SB_USER_TYPE_TIER_1 or request.user.Profile_User.privilege_id.user_type == settings.SB_USER_TYPE_TIER_2:
        return HttpResponse("<h1>Error: 403 Forbidden</h1>")

    try:
        requested_username = request.POST['requestId']
        requested_action = request.POST['status']

        requested_user = User.objects.get(username=requested_username)
        requested_profile = Profile.objects.get(user=requested_user, flag=False)
        if requested_action == "approve":
            #approve profile and default bank account
            bank_acct = Account.objects.get(user=requested_user)
            requested_profile.flag=True
            bank_acct.flag = True
            requested_profile.save()
            bank_acct.save()

        elif requested_action == "reject":
            requested_user.delete()

        return HttpResponse("200")

    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return HttpResponse("404")
    except KeyError:
        return HttpResponse("400")

def _updateRequest(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if not request.method == 'POST':
        return HttpResponse("<h1>Error: 400 Bad Request</h1>")
    try:

        if request.POST['requestType'] == 'user_registration': #user regsitration approval
            return handleUserRegistrationApproval(request)
            '''
        elif : #critical transaction request
            return handleCriticalTransactionApproval(request)
            '''
        else:
            return HttpResponse("<h1>Error: 400 Bad Request</h1>")

    except KeyError:
        return HttpResponse("<h1>Error: 400 Bad Request</h1>")

