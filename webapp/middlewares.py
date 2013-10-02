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

class AngularCSRFRename(object):
    ANGULAR_HEADER_NAME = 'HTTP_X_XSRF_TOKEN'
    def process_request(self, request):
        if self.ANGULAR_HEADER_NAME in request.META:
            request.META['HTTP_X_CSRFTOKEN'] = request.META[self.ANGULAR_HEADER_NAME]
            del request.META[self.ANGULAR_HEADER_NAME]
        return None

# EOF
