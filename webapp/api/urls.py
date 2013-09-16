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
# Last mod : 16-Aug-2013
# -----------------------------------------------------------------------------
from django.conf.urls import patterns, url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'countries'           , views.CountryViewSet, base_name="countries")
router.register(r'currencies'          , views.CurrencyViewSet)
router.register(r'meta'                , views.MetaViewSet     , base_name="meta")
router.register(r'stories'             , views.StoryViewSet)
router.register(r'stories-nested'      , views.StoryNestedViewSet,  base_name="stories-nested")
router.register(r'themes'              , views.ThemeViewSet)
router.register(r'filters/themes'      , views.UsedThemeViewSet,    base_name="used themes")
router.register(r'filters/countries'   , views.UsedCountryViewSet,  base_name="used countries")
router.register(r'filters/currencies'  , views.UsedCurrencyViewSet,  base_name="used currencies")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    # url(r'^meta/$', views.MetaView.as_view(), name='meta'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^', include(router.urls))
)
# EOF
