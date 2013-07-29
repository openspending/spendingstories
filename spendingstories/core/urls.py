from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^stories/$', views.index, name='stories-list'),
)
