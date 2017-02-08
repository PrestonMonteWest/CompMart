from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

app_name = 'commerce'

urlpatterns = [
    url(r'^product/(?P<pk>[1-9]\d*)/$', views.Details.as_view(), name='product'),
    url(r'^login/$', login, {'template_name': 'commerce/login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^add/(?P<pk>[1-9]\d*)/$', views.add, name='add'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^register/$', views.Register.as_view(), name='register'),
]
