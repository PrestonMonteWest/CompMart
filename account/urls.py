from django.urls import reverse_lazy
from django.conf.urls import url, include
from . import views

app_name = 'account'

addresses = [
    url(r'^$', views.AddressList.as_view(), name='addresses'),
    url(r'^add_address/$', views.add_address, name='add_address'),
    url(
        r'^edit_address/(?P<pk>[1-9]\d*)/$',
        views.edit_address,
        name='edit_address'
    ),
    url(
        r'^delete_address/(?P<pk>[1-9]\d*)/$',
        views.DeleteAddress.as_view(),
        name='delete_address'
    ),
]

cards = [
    url(r'^$', views.CardList.as_view(), name='cards'),
    url(r'^add_card/$', views.add_card, name='add_card'),
    url(r'^edit_card/(?P<pk>[1-9]\d*)/$', views.edit_card, name='edit_card'),
    url(
        r'^delete_card/(?P<pk>[1-9]\d*)/$',
        views.DeleteCard.as_view(),
        name='delete_card'
    ),
]

orders = [
    url(r'^$', views.OrderList.as_view(), name='orders'),
    url(r'^order/(?P<pk>[1-9]\d*)/$', views.OrderDetails.as_view(), name='order'),
]

reviews = [
    url(r'^$', views.ReviewList.as_view(), name='reviews'),
    url(r'^edit_review/(?P<pk>[1-9]\d*)/$', views.edit_review, name='edit_review'),
    url(
        r'^delete_review/(?P<pk>[1-9]\d*)/$',
        views.DeleteReview.as_view(),
        name='delete_review'
    ),
]

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
    url(r'^addresses/', include(addresses)),
    url(r'^cards/', include(cards)),
    url(r'^orders/', include(orders)),
    url(r'^reviews/', include(reviews)),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.Register.as_view(), name='register'),
]
