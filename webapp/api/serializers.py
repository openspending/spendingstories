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
from rest_framework import serializers
from webapp.currency.models import Currency
from webapp.core.models import Story, Theme

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story

class StoryNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        depth = 1
        # NOTE: because of `depth = 1`. It disalow writing on foreign keys
        read_only_fields = ('currency', 'themes')

# EOF
