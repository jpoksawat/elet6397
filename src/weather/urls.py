from django.conf.urls import url

from . import views

app_name = 'weather'
urlpatterns = [
    url(r'^push/$', views.push, name='push'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^temperature/(?P<sensor_id>[0-9]+)/$', views.temperature_detail, name='temperature_detail'),
    url(r'^temperature/(?P<sensor_id>[0-9]+)/chart/$', views.temperature_chart, name='temperature_chart'),
    url(r'^humidity/(?P<sensor_id>[0-9]+)/$', views.humidity_detail, name='humidity_detail'),
    url(r'^humidity/(?P<sensor_id>[0-9]+)/chart/$', views.humidity_chart, name='humidity_chart'),
]
