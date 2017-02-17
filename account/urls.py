from django.shortcuts import reverse
from django.views.generic import CreateView
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from . import views

app_name = 'account'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    url(
        r'^password_change/$',
        auth_views.password_change,
        {
            'template_name': 'account/password_change.html',
            'post_change_redirect': 'account:password_change_done',
        },
        name='password_change'
    ),
    url(
        r'^password_change_done/$',
        auth_views.password_change_done,
        {'template_name': 'account/password_change_done.html'},
        name='password_change_done'
    ),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', CreateView.as_view(
        template_name='account/register.html',
        form_class=UserCreationForm,
        success_url='/'
    ), name='register'),
]
