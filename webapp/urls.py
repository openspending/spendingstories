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
