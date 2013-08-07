#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 07-Aug-2013
# Last mod : 07-Aug-2013
# -----------------------------------------------------------------------------
from django import forms

class SelectAutoComplete(forms.widgets.Select):

    class Media:
        css = {
            'all': ("css/ui-lightness/jquery-ui-1.10.3.custom.min.css",)
        }
        js = ("js/jquery-1.9.1.js", "js/jquery-ui-1.10.3.custom.min.js", "js/admin-story-script.js")

    def render(self, name, value, attrs=None, choices=()):
        if attrs is None:
            attrs = {}
        attrs['class'] = "combobox"
        return super(SelectAutoComplete, self).render(name, value, attrs, choices)

# EOF
