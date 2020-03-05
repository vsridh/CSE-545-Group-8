from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect


class TimeOutLogin:
    def process_request(self, request):
        if request.user.is_authenticated:
            last_activity = datetime.strptime(request.session['last_activity'], "%m/%d/%Y, %H:%M:%S")
            try:
                if datetime.now() - last_activity > timedelta(0, settings.AUTO_LOGOUT_DELAY_MINS * 60, 0):
                    auth.logout(request)
                    del request.session['last_activity']
                    return HttpResponseRedirect('/login/')
            except KeyError:
                pass

            request.session['last_activity'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        return None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        resp = self.process_request(request)
        if resp is not None:
            return resp
        else:
            return self.get_response(request)

