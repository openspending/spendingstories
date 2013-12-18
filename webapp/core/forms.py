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
# Last mod : 06-Aug-2013
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

from django import forms
from webapp.core.models import Story
from webapp.currency.models import Currency
import datetime
import widgets
import fields
from redactor.widgets import RedactorEditor
import inflation

class StoryForm(forms.ModelForm):

    country  = forms.CharField(
        widget      = widgets.SelectAutoComplete(choices = fields.COUNTRIES))
    currency = forms.ModelChoiceField(
        widget      = widgets.SelectAutoComplete(choices = fields.COUNTRIES),
        queryset    = Currency.objects.all(),
        empty_label = "(currency)")

    class Meta:
        model = Story
        verbose_name_plural = "stories"

    def clean_year(self):
        year  = self.cleaned_data['year']
        years = sorted(inflation.available_years()[self.cleaned_data['country']])
        if not year in years and year != datetime.date.today().year:
            raise forms.ValidationError("This year is not available to compute the inflated value. Dates available: %s" % years)
        return year

# -----------------------------------------------------------------------------
#
#    PAGE
#
# -----------------------------------------------------------------------------
class PageForm(forms.ModelForm):
    title   = forms.CharField()
    slug    = forms.CharField()
    content = forms.CharField(widget=RedactorEditor(allow_file_upload=False,allow_image_upload=False))

# EOF
