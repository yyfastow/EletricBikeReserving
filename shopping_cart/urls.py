from django.conf.urls import url

from shopping_cart import views

urlpatterns = [
    url(r'^$', views.show_cart, name='cart'),
    url(r'remove/(?P<pk>\d+)/$', views.remove_item_in_cart, name='remove'),
    url(r'update cart/$', views.update_cart, name='update'),
    url(r'change amount/(?P<pk>\d+)/$', views.change_amount, name='change_amount'),
    url(r'(?P<pk>\d+)/$', views.add_to_cart, name='add_to_cart'),
]