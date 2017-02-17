from django.conf.urls import url
from . import views

app_name = 'commerce'

urlpatterns = [
    url(r'^product/(?P<pk>[1-9]\d*)/$', views.Details.as_view(), name='product'),
    url(r'^add/(?P<pk>[1-9]\d*)/$', views.add, name='add'),
    url(r'^cart/$', views.cart, name='cart'),
]
