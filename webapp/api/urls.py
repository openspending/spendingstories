#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 06-Aug-2013
# Last mod : 16-Aug-2013
# -----------------------------------------------------------------------------
# This file is part of Spending Stories.
# 
#     Spending Stories is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Spending Stories is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Spending Stories.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'countries'           , views.CountryViewSet     , base_name="countries"      )
router.register(r'currencies'          , views.CurrencyViewSet    , base_name="currencies"     )
router.register(r'meta'                , views.MetaViewSet        , base_name="meta"           )
router.register(r'stories'             , views.StoryViewSet       , base_name="stories"        )
router.register(r'stories-nested'      , views.StoryNestedViewSet , base_name="stories-nested" )
router.register(r'themes'              , views.ThemeViewSet       , base_name="themes"         )
router.register(r'filters'             , views.FiltersViewSet     , base_name="filters"        )
router.register(r'pages'               , views.PagesViewSet       , base_name="pages"          )

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^', include(router.urls))
)
# EOF
