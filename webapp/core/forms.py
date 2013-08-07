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
# Last mod : 06-Aug-2013
# -----------------------------------------------------------------------------
from django import forms
from webapp.core.models import Story
from webapp.currency.models import Currency
import json
import os
from django.conf import settings
import datetime
import widgets
import fields

AVAILABLE_YEAR_PER_COUNTRY = json.load(file(os.path.join(settings.ROOT_PATH, 'data/years_available_per_country.json')))

class StoryForm(forms.ModelForm):

	country  = forms.CharField(
		widget      = widgets.SelectAutoComplete(choices = fields.COUNTRIES))
	currency = forms.ModelChoiceField(
		widget      = widgets.SelectAutoComplete(choices = fields.COUNTRIES),
		queryset    = Currency.objects.all(),
		empty_label = "(currency)")

	class Meta:
		model = Story

	def clean_year(self):
		year  = self.cleaned_data['year']
		years = sorted(AVAILABLE_YEAR_PER_COUNTRY[self.cleaned_data['country']])
		if not year in years and year != datetime.date.today().year:
			raise forms.ValidationError("For this country, are available: %s" % years)
		return year

# EOF
