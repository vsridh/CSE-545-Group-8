from django.urls import path
from . import views
from django.conf.urls import url

app_name = "internal_homepage"

urlpatterns = [
    path('', views.internal_homepage, name = 'create_internal_account_homepage'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    views.activate, name='activate'),
]