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

from rest_framework import serializers 
from webapp.currency.models import Currency
from webapp.core.models import Story, Theme

class ThemeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    class Meta:
        model = Theme

    def get_image(self, obj):
        """ return the absolute image url """
        return obj.image.url

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story

class StoryNestedSerializer(StorySerializer):
    themes   = ThemeSerializer(many=True, read_only=True)
    currency = CurrencySerializer(read_only=True)
    class Meta:
        model = Story

# EOF

