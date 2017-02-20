from django.conf.urls import url
from . import views

app_name = 'commerce'

urlpatterns = [
    url(
        r'^product/(?P<pk>[1-9]\d*)/$',
        views.ProductDetails.as_view(),
        name='product'
    ),
    url(
        r'^add_product/(?P<pk>[1-9]\d*)/$',
        views.add_product,
        name='add_product'
    ),
    url(
        r'^delete_product/(?P<pk>[1-9]\d*)/$',
        views.delete_product,
        name='delete_product'
    ),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
]
