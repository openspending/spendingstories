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

class StoryForm(forms.ModelForm):
	class Meta:
		model = Story

	def clean(self):
		cleaned_data = super(StoryForm, self).clean()
		return cleaned_data

# EOF
