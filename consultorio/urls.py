from django.conf.urls import url

from . import views

app_name = 'consultorio'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^newPaciente/$', views.newPaciente, name='newPaciente'),
    url(r'^listPaciente/$', views.listPaciente, name='listPaciente'),
    url(r'^viewPaciente/$', views.viewPaciente, name='viewPaciente'),
    url(r'^viewConsulta/$', views.viewConsulta, name='viewConsulta'),
    url(r'^editPaciente/(?P<pk>\d+)/$', views.editPaciente, name='editPaciente'),
    url(r'^detailPaciente/(?P<pk>\d+)/$', views.detailPaciente, name='detailPaciente'),
    url(r'^newConsulta/(?P<pk>\d+)/$', views.newConsulta, name='newConsulta'),
    url(r'^editConsulta/(?P<pk>\d+)/$', views.editConsulta, name='editConsulta'),
    url(r'^detailConsulta/(?P<pk>\d+)/$', views.detailConsulta, name='detailConsulta'),
    
]
