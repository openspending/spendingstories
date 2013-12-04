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
# Last mod : 09-Aug-2013
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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
import models
import forms

# -----------------------------------------------------------------------------
#
#    THEME
#
# -----------------------------------------------------------------------------
class ThemeAdmin(admin.ModelAdmin):
    list_display        = ('title', 'description', 'image_tag', 'active')
    prepopulated_fields = {"slug": ("title",)}
    list_editable       = ('active',)
    list_filter         = ('active',)

# -----------------------------------------------------------------------------
#
#    STORY
#
# -----------------------------------------------------------------------------
def make_published(modeladmin, request, queryset):
    queryset.update(status='published')
make_published.short_description = _("Mark selected contributions as published")

def make_refused(modeladmin, request, queryset):
    queryset.update(status='refused')
make_refused.short_description = _("Mark selected contributions as refused")

def make_pending(modeladmin, request, queryset):
    queryset.update(status='pending')
make_pending.short_description = _("Mark selected contributions as pending")

class StoryAdmin(admin.ModelAdmin):
    actions           = [make_published, make_refused, make_pending]
    list_display      = ('title', 'value', 'current_value_usd', 'currency', 'country','year', 'sticky', 'created_at', 'type', 'lang', 'status')
    readonly_fields   = ('current_value', 'current_value_usd', 'inflation_last_year', 'created_at')
    search_fields     = ('title', 'value', 'current_value_usd', 'country')
    list_editable     = ('sticky',)
    list_filter       = ('status', 'sticky', 'type', 'themes', 'currency', 'country', 'lang')
    filter_horizontal = ('themes',)
    form              = forms.StoryForm
    fieldsets         = (
        ("Admin fields", {
            'fields': ('status','lang', 'sticky', 'title', 'description', 'source', 'value', 'currency', 'country', 'year', 'type', 'themes', 'extras')
        }),
        ('Auto computed fields', {
            'fields': readonly_fields
        }),
    )

    class Media:
        css = {
            'all': ("css/vendor/ui-lightness/jquery-ui-1.10.3.custom.min.css",)
        }
        js = ("js/vendor/jquery-1.9.1.js", "js/vendor/jquery-ui-1.10.3.custom.min.js", "js/admin-story-script.js")


# -----------------------------------------------------------------------------
#
#    PAGE
#
# -----------------------------------------------------------------------------
class PageAdmin(admin.ModelAdmin):
    list_display    = ('title',)
    form            = forms.PageForm

admin.site.register(models.Story, StoryAdmin)
admin.site.register(models.Theme, ThemeAdmin)
admin.site.register(models.Page, PageAdmin)

# EOF
