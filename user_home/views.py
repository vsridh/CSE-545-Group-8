from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
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