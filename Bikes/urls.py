from django.conf.urls import url

from Bikes import views

urlpatterns = [
    url(r'^$', views.bike_type_list, name="type"),

    url(r'superuser/$', views.admin_orders, name="all_orders"),
    url(r'superuser/message/$', views.admin_send_message, name='admin_message'),
    url(r'superuser/ready to ship/$', views.orders_ready_to_ship, name="admin_shipping"),
    url(r'superuser/mark shipped/$', views.shipping_order, name="mark shipped"),
    url(r'superuser/received/(?P<pk>\d+)/$', views.recieved_order, name="recieved"),
    url(r'superuser/(?P<pk>\d+)/$', views.admin_user_preorders, name="users_orders"),
    # url(r'superuser/bike/(?P<pk>\d+)$', views.admin_orders_bike, name="bike_ordered"),
    url(r'superuser/change amount/$', views.change_reservation_amount, name="change_reservation_amount"),

    url(r'user/$', views.users_orders, name='user'),
    # url(r'user/ready/$', views.users_orders_ready, name='ready'),
    # url(r'user/ready/(?P<pk>\d+)/$', views.ready_order_details, name='shipping'),
    # url(r'user/shipped/(?P<pk>\d+)/$', views.sending_order_details, name='shipped'),
    url(r'user/edit address/$', views.edit_address, name='edit_address'),
    url(r'user/change address/$', views.change_address, name='change_address'),
    url(r'user/edit card/$', views.edit_card, name='edit_card'),
    url(r'user/change card/$', views.change_card, name='change_card'),
    # url(r'user/edit cards/$', views.edit_cards, name='edit_cards'),
    url(r'user/(?P<pk>\d+)/$', views.order_details, name='order_detail'),
    url(r'user/edit/$', views.edit_order, name='edit'),
    # url(r'user/change password/$', views.change_password, name='change_password'),
    url(r'user/cancel order/$', views.cancel_order, name='cancel'),
    url(r'user/cancel orders/$', views.cancel_all_orders, name='cancel_all'),
    url(r'user/add address/$', views.add_address, name="add_address"),
    url(r'user/add card/$', views.add_card, name="add_card"),

    url(r'first checkout/$', views.first_checkout, name='first_checkout'),
    url(r'checkout/$', views.checkout, name='checkout'),


    url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/$', views.bike_details, name='details'),
    # url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/order/$', views.order_bike, name='order'),
    # url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/order more/$', views.order_another_bike, name='order_more'),
    url(r'(?P<pk>\d+)/$', views.bike_list, name='list'),
]