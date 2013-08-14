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

class StorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Story
        depth = 1

class ThemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Theme

class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency

# EOF
