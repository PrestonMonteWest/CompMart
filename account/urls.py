from django.shortcuts import reverse
from django.views.generic import CreateView
from django.conf.urls import url
from django.contrib.auth.views import login, password_change
from django.contrib.auth.forms import UserCreationForm
from . import views

app_name = 'account'

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^password_change/$',
        password_change,
        {'template_name': 'account/password.html'},
        name='password_change'
    ),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', CreateView.as_view(
        template_name='account/register.html',
        form_class=UserCreationForm,
        success_url='/'
    ), name='register'),
]
