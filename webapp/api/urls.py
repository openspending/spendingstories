#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 06-Aug-2013
# Last mod : 14-Aug-2013
# -----------------------------------------------------------------------------
from django.conf.urls import patterns, url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'stories'       , views.StoryViewSet)
router.register(r'stories-nested', views.StoryNestedViewSet, base_name="stories-nested")
router.register(r'themes'        , views.ThemeViewSet)
router.register(r'currencies'    , views.CurrencyViewSet)
router.register(r'meta'          , views.MetaViewSet, base_name="meta")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    # url(r'^meta/$', views.MetaView.as_view(), name='meta'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls))
)

# EOF
