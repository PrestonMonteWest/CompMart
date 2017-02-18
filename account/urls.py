from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url
from . import views

app_name = 'account'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(
        r'^login/$',
        views.login,
        {'template_name': 'account/login.html'},
        name='login'
    ),
    url(
        r'^password_change/$',
        views.password_change,
        {
            'template_name': 'account/password_change.html',
            'post_change_redirect': 'account:password_change_done',
            'extra_context': {'success': False},
        },
        name='password_change'
    ),
    url(
        r'^password_change_done/$',
        views.password_change,
        {
            'template_name': 'account/password_change.html',
            'post_change_redirect': 'account:password_change_done',
            'extra_context': {'success': True},
        },
        name='password_change_done'
    ),
    url(r'^add_address/$', views.add_address, name='add_address'),
    url(
        r'^add_address_done/$',
        views.add_address,
        {'success': True},
        name='add_address_done'
    ),
    url(r'^add_card/$', views.add_card, name='add_card'),
    url(
        r'^add_card_done/$',
        views.add_card,
        {'success': True},
        name='add_card_done'
    ),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.Register.as_view(), name='register'),
]
