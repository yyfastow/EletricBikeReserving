from django.conf.urls import url

from Bikes import views

urlpatterns = [
    url(r'^$', views.bike_type_list, name='type'),
    url(r'login/$', views.loginer, name='login'),
    url(r'logout/$', views.logout_view, name='logout'),
    url(r'user/$', views.users_orders, name='user'),
    url(r'user/(?P<pk>\d+)/$', views.order_details, name='order_detail'),
    url(r'user/edit/$', views.edit_order, name='edit'),
    url(r'user/change password/$', views.change_password, name='change_password'),
    url(r'user/(?P<pk>\d+)/cancel order/$', views.cancel_order, name='cancel'),

    url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/$', views.bike_details, name='details'),
    url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/order/$', views.order_bike, name='order'),
    url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/order more/$', views.order_another_bike, name='order_more'),
    url(r'(?P<pk>\d+)/$', views.bike_list, name='list'),
]