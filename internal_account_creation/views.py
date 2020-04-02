from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import ExtendedUserCreationForm, UserProfileForm, TierStatus
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from home.models import Privilege
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.encoding import force_text

def internal_homepage(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        tier =TierStatus(request.POST)
        if form.is_valid() and profile_form.is_valid() and tier.is_valid():
            user= form.save()
            user.save()
            acc=tier.save(commit=False)
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.privilege_id=Privilege.objects.get(user_type=acc)
            acc.user=profile.user
            profile.save()
            acc.save()
            current_site = get_current_site(request)
            print(current_site)
            mail_subject = 'Activate your bank account.'
            message = render_to_string('acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token':force_text(account_activation_token.make_token(user)),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponseRedirect('/login/')
    else:
        form=ExtendedUserCreationForm()
        profile_form=UserProfileForm()
        tier=TierStatus()

    context={'form' : form, 'profile_form' : profile_form, 'tier' : tier}
    return render(request,'internal_register.html',context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponse('Activation link is invalid!')
# Create your views here.