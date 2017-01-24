from django.conf.urls import url
from . import views

app_name = 'commerce'

# trailing slash is optional to reduce redirection
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product/(?P<pk>[1-9]\d*)/?$', views.product, name='product'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
]
