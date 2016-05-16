from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_hospital', views.add_hospital, name='add_hospital'),
    url(r'^hospital/(?P<hospital_name_slug>[\w\-]+)/$', views.hospital, name='hospital'),
    url(r'^profile/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<profile_name>[\w\-]+)/$', views.profile, name='profile'),
]
