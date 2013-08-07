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
# Last mod : 07-Aug-2013
# -----------------------------------------------------------------------------
from django.contrib import admin
import models
import forms

class ThemeAdmin(admin.ModelAdmin):
    list_display    = ('title', 'description', 'active')
    prepopulated_fields = {"slug": ("title",)}
    list_editable       = ('active',)

class StoryAdmin(admin.ModelAdmin):
    list_display    = ('title', 'value', 'currency', 'current_value_usd', 'continuous', 'country', 'sticky', 'status')
    readonly_fields = ('current_value', 'current_value_usd', 'inflation_last_year',)
    search_fields   = ('title', 'value', 'current_value_usd', 'country')
    list_editable   = ('sticky', 'status')
    form            = forms.StoryForm

admin.site.register(models.Story, StoryAdmin)
admin.site.register(models.Theme, ThemeAdmin)

# EOF
