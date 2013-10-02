#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 07-Aug-2013
# Last mod : 07-Aug-2013
# -----------------------------------------------------------------------------
"""
Heroku environment variables:
AWS_ACCESS_KEY_ID:       <AWS_KEY>
AWS_SECRET_ACCESS_KEY:   <AWS_PWD>
AWS_STORAGE_BUCKET_NAME: <BUCKET_NAME>
BUILDPACK_URL:           git://github.com/vied12/heroku-buildpack-django.git
HEROKU:                  True
PATH:                    bin:node_modules/.bin:/app/bin:/usr/local/bin:/usr/bin:/bin
PYTHONPATH:              webapp/:libs/
DATABASE_URL             postgres://<POSTGRES_URL>
"""
HEROKU = True

from settings import *

DEBUG = False

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

INSTALLED_APPS         += ('storages',)
DEFAULT_FILE_STORAGE    = 'storages.backends.s3boto.S3BotoStorage'
# Static storage
STATICFILES_STORAGE     = DEFAULT_FILE_STORAGE
AWS_ACCESS_KEY_ID       = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY   = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_QUERYSTRING_AUTH    = False
AWS_S3_FILE_OVERWRITE   = True
STATIC_URL              = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

COMPRESS_URL            = STATIC_URL
COMPRESS_STORAGE        = STATICFILES_STORAGE

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
# Activate CSS minifier in
COMPRESS_CSS_FILTERS = (
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
)