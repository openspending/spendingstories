from django.conf.urls import patterns, include, url
from rest_framework   import generics
import views


urlpatterns = patterns('',
    url(r'^$', views.api_root_view, name='api-root'),
    url(r'^stories/?$', views.StoryListAPIView.as_view(), name='stories-list'),
    url(r'^stories/proximity/?', views.ProximityStoryListAPIView.as_view(), name='proximity-stories-list'), 
    url(r'^stories/(?P<pk>[0-9]+)/?$', views.StoryDetailsAPIView.as_view(), name='story-details'),
)
