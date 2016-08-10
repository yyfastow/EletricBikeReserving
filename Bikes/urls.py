from django.conf.urls import url

from Bikes import views

urlpatterns = [
    url(r'^$', views.bike_type_list, name='type'),
    url(r'login/$', views.loginer, name='login'),
    url(r'logout/$', views.logout_view, name='logout'),
    url(r'message/$', views.message, name="message"),

    url(r'superuser/$', views.admin_orders, name="all_orders"),
    url(r'superuser/message/(?P<pk>\d+)/$', views.admin_send_message, name='admin_message'),
    url(r'superuser/ready to ship/$', views.orders_ready_to_ship, name="shipping"),
    url(r'superuser/ready to ship/(?P<pk>\d+)/$', views.shipping_order, name="shipped"),
    url(r'superuser/recieved/(?P<pk>\d+)/$', views.recieved_order, name="recieved"),
    url(r'superuser/(?P<pk>\d+)/$', views.admin_user_preorders, name="users_orders"),
    url(r'superuser/bike/(?P<pk>\d+)$', views.admin_orders_bike, name="bike_ordered"),

    url(r'user/$', views.users_orders, name='user'),
    url(r'user/ready/$', views.users_orders_ready, name='ready'),
    url(r'user/edit address/(?P<pk>\d+)/$', views.edit_address, name='edit_address'),
    url(r'user/edit card/(?P<pk>\d+)/$', views.edit_card, name='edit_card'),
    url(r'user/edit cards/$', views.edit_cards, name='edit_cards'),
    url(r'user/(?P<pk>\d+)/$', views.order_details, name='order_detail'),
    url(r'user/edit/$', views.edit_order, name='edit'),
    url(r'user/change password/$', views.change_password, name='change_password'),
    url(r'user/(?P<pk>\d+)/cancel order/$', views.cancel_order, name='cancel'),
    url(r'user/add address/$', views.add_address, name="add_address"),
    url(r'user/add card/$', views.add_card, name="add_card"),

    url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/$', views.bike_details, name='details'),
    url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/order/$', views.order_bike, name='order'),
    url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/order more/$', views.order_another_bike, name='order_more'),
    url(r'(?P<pk>\d+)/$', views.bike_list, name='list'),
]