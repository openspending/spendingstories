#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 08-Aug-2013
# Last mod : 08-Aug-2013
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

from django.conf.urls        import patterns, include, url
from django.conf             import settings
from django.contrib          import admin
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',    
    # Our main views URL, see webapp.core.urls
    # url(r'^',           include('webapp.core.urls')),
    # API & API documentation urls 
    url(r'^api/',       include('webapp.api.urls')),
    url(r'^api-docs/',  include('rest_framework_docs.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/',     include(admin.site.urls)),
    url(r'^$', 			'webapp.core.views.home', name='home'),    
    url(r'^partial/(?P<partial_name>([a-zA-Z0-9_\-/]+))\.html$', 'webapp.core.views.partial', name='partial'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # serving media folder in debug mode
