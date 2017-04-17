from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_hospital', views.CreateHospital.as_view(), name='add_hospital'),
    url(r'^add_disease_n_category', views.CreateDiseaseView.as_view(), name='add_disease'),
    url(r'^hospital/(?P<hospital_name_slug>[\w\-]+)/$', views.HospitalView.as_view(), name='hospital'),
    url(r'^profile/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<profile_name>[\w\-]+)/$', views.DoctorProfileView.as_view(), name='profile'),
    url(r'^disease/(?P<pk>[\w\-]+)/$', views.DiseaseView.as_view(), name='disease'),
    url(r'^like_doc/$', views.like_doc, name='like_doc'),
    url(r'^suggest_disease/$', views.suggest_disease, name='suggest_disease'),
]
