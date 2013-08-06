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
from webapp.core.models import Story, Theme
from django.utils.translation import ugettext_lazy as _
import json
import os
from django.conf import settings

AVAILABLE_YEAR_PER_COUNTRY = json.load(file(os.path.join(settings.ROOT_PATH, 'data/years_available_per_country.json')))

class StoryForm(forms.ModelForm):
	class Meta:
		model = Story

	def clean(self):
		cleaned_data = super(StoryForm, self).clean()
		return cleaned_data

	def clean_year(self):
		year  = self.cleaned_data['year']
		years = AVAILABLE_YEAR_PER_COUNTRY[self.cleaned_data['country']]
		print year, years
		if not year in years:
			raise forms.ValidationError("For this country, are available: %s" % ", ".join(years))
		return year


# EOF
