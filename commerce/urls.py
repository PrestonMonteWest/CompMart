from django.conf.urls import url
from . import views

app_name = 'commerce'

urlpatterns = [
    url(r'^(?P<page>[1-9]\d*)?$', views.Index.as_view(), name='index'),
    url(r'^product/(?P<pk>[1-9]\d*)/$', views.Details.as_view(), name='product'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^add/(?P<pk>[1-9]\d*)/$', views.add, name='add'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^register/$', views.register, name='register'),
]
