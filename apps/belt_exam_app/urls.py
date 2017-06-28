from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^create_user$', views.create_user),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add_trip),
    url(r'^create_trip$', views.create_trip),
    url(r'^join_trip/(?P<id>\d+)$', views.join_trip),
    url(r'^view_dest/(?P<id>\d+)$', views.view_dest)


]
