from django.conf.urls import url

from Bikes import views

urlpatterns = [
    url(r'^$', views.bike_type_list, name='type'),
    url(r'(?P<types_pk>\d+)/(?P<bike_pk>\d+)/$',
        views.bike_details,
        name='details'),
    url(r'(?P<pk>\d+)/$', views.bike_list, name='list'),
]