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
# Last mod : 15-Aug-2013
# -----------------------------------------------------------------------------
from rest_framework import serializers, filters 
from webapp.currency.models import Currency
from webapp.core.models import Story, Theme

class UsedModelSerializer(serializers.ModelSerializer):
    used = serializers.SerializerMethodField('is_used')
    def is_used(self, obj):
        meta = self.__class__.ModelMeta()
        kwargs = { meta.queryset_filter: getattr(obj, meta.attribute) }
        return meta.queryset.filter(**kwargs).count() > 0

class UsedModelFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        serializer_class = view.serializer_class()
        results = []
        is_used = request.QUERY_PARAMS.get('isUsed', None)
        if not isinstance(serializer_class, UsedModelSerializer) or is_used is None:
            results = queryset
        else:
            b_is_used = is_used != 'False' and is_used != 'false'
            for elem in queryset:
                if view.serializer_class().is_used(elem) == b_is_used:
                    results.append(elem)
        return results

class ThemeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    class Meta:
        model = Theme

    def get_image(self, obj):
        """ return the absolute image url """
        return obj.image.url

class UsedThemeSerializer(ThemeSerializer, UsedModelSerializer):
    class ModelMeta: 
        attribute = 'slug'
        queryset_filter = 'themes__slug'
        queryset = Story.objects.public()

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency

class UsedCurrencySerializer(CurrencySerializer, UsedModelSerializer):
    class ModelMeta:
        queryset = Story.objects.public() 
        attribute = 'iso_code'
        queryset_filter = 'currency'

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story

class StoryNestedSerializer(StorySerializer):
    themes   = ThemeSerializer(many=True, read_only=True)
    currency = CurrencySerializer(read_only=True)
    class Meta:
        model = Story

# EOF

