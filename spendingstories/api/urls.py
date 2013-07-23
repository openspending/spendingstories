from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
import views


rooter = DefaultRouter() 
rooter.register(r'^spending', views.SpendingViewSet)
urlpatterns = patterns('',
   url(r'^', include(rooter.urls)),
    # url(r'^spending/(?P<pk>[0-9]+)/compare$', views.SpendingDetailsComparing.as_view()),
)
