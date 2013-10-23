#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 21-Aug-2013
# Last mod : 21-Aug-2013
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


class AngularCSRFRename(object):
    """ 
    * The CSRF HTTP header name can't be changed in Django (must be X-CSRFToken)
    * The CSRF HTTP header name can't be changed in Angular (must be X-XSRF-TOKEN)
    * The CSRF cookie name can't be changed in Angular (must be XSRF-TOKEN)
    
    So to get the Django and AngularJS CSRF/XSRF implementations to play nicely together, 
    we have to get Django to send a properly-named CSRF cookie (the cookie name is configurable, thankfully) 
    and make it aware of AngularJS's X-XSRF-TOKEN header by copying it to X-CSRFToken in request.META

        From http://bluehat.us/posts/django-angularjs-and-csrf-xsrf-protection.html
    """

    ANGULAR_HEADER_NAME = 'HTTP_X_XSRF_TOKEN'

    def process_request(self, request):
        if self.ANGULAR_HEADER_NAME in request.META:
            request.META['HTTP_X_CSRFTOKEN'] = request.META[self.ANGULAR_HEADER_NAME]
            del request.META[self.ANGULAR_HEADER_NAME]
        return None

# EOF
