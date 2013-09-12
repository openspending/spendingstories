#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 12-Sept-2013
# Last mod : 12-Sept-2013
# -----------------------------------------------------------------------------
from rest_framework import filters
from webapp.core.models import Story, Theme

class IsUsedInStoriesFilter(filters.BaseFilterBackend):
    stories = Story.objects.public()
    
    def filter_queryset(self, request, queryset, view):
        if 'usedInStories' in request.QUERY_PARAMS:
            results = []
            meta_args = self.__class__.Meta()
            for obj in queryset:
                kwargs = {}
                kwargs[meta_args.model_filter] = getattr(obj, meta_args.attr)
                if len(self.stories.filter(**kwargs)) > 0:
                    results.append(obj)
            return results
        else:
            return queryset

class UsedThemes(IsUsedInStoriesFilter):
    class Meta:
        model   = Theme
        attr    = 'slug'
        model_filter = '{0}__{1}'.format('themes', attr)


class UsedCurrencies(IsUsedInStoriesFilter):
    class Meta:
        attr = 'iso_code'
        model_filter = '{0}__{1}'.format('currency', attr)
