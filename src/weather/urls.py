from django.conf.urls import url

from . import views

app_name = 'weather'
urlpatterns = [
    url(r'^push/$', views.push, name='push'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<sensor_id>[0-9]+)/(?P<field>\w+)/$', views.detail, name='detail'),
    url(r'^(?P<sensor_id>[0-9]+)/(?P<field>\w+)/chart/$$', views.chart, name='chart'),
]
