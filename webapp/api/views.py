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
# Last mod : 16-Aug-2013
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

from webapp.core.models      import Story, Theme
from webapp.currency.models  import Currency
from rest_framework          import viewsets
from rest_framework.response import Response
from rest_framework          import permissions
from django.db.models        import Max, Min, Q
from relevance               import Relevance
from viewsets                import ChoicesViewSet

import serializers

# -----------------------------------------------------------------------------
#
#    STORIES
#
# -----------------------------------------------------------------------------
class StoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True
        elif request.method == 'DELETE':
            # Check permissions for delete request
            if request.user and request.user.is_staff:
                return True
            else:
                return False
        else:
            # Check permissions for write request
            return True

class StoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows story to be viewed or edited.
    """
    queryset           = Story.objects.public()
    serializer_class   = serializers.StorySerializer
    filter_fields      = ('sticky', 'country', 'currency','type',)
    permission_classes = (StoryPermission,)

    def get_queryset(self):
        queryset = self.queryset
        if 'themes' in self.request.QUERY_PARAMS:
            themes = self.request.QUERY_PARAMS['themes'].split(',')
            qg = None 
            for theme in themes:
                if qg is None:
                    qg = Q(themes__slug=theme)
                else:
                    qg |= Q(themes__slug=theme)

            queryset = queryset.filter(qg).distinct()
        if 'title' in self.request.QUERY_PARAMS:
            print self.request.QUERY_PARAMS['title']
            queryset = queryset.filter(title=self.request.QUERY_PARAMS['title']).distinct()
        return queryset

    def create(self, request, pk=None):
        # reset reserved field if not staff
        if not request.user or not request.user.is_staff:
            request.DATA['status'] = "pending"
            request.DATA['sticky'] = False
        response = super(StoryViewSet, self).create(request, pk)
        return response

    def list(self, request, *args, **kwargs):
        """ Contains the code to add the relevance if needed """
        response      = super(StoryViewSet, self).list(request, *args, **kwargs)
        relevance_for = request.QUERY_PARAMS.get('relevance_for')
        if relevance_for:
            for i, story in enumerate(response.data):
                score, _type, value, ratio = Relevance().compute(
                    amount      = relevance_for,
                    compared_to = story['current_value_usd'],
                    story_type  = story['type'])
                story['relevance_score'] = score
                story['relevance_type' ] = _type
                story['relevance_value'] = value
                story['relevance_ratio'] = ratio
                response.data[i] = story
            # order by relevance score
            response.data = sorted(response.data, cmp=lambda x,y: cmp(y['relevance_score'], x['relevance_score']))
        return response

class StoryNestedViewSet(StoryViewSet):
    """
    API endpoint that allows story to be viewed in a nested mode.
    """
    serializer_class = serializers.StoryNestedSerializer

# -----------------------------------------------------------------------------
#
#    THEME
#
# -----------------------------------------------------------------------------
class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Theme to be viewed or edited.
    """
    queryset         = Theme.objects.public()
    serializer_class = serializers.ThemeSerializer

# -----------------------------------------------------------------------------
#
#    CURRENCY
#
# -----------------------------------------------------------------------------
class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Currency to be viewed or edited.
    """
    queryset         = Currency.objects.all()
    serializer_class = serializers.CurrencySerializer

# -----------------------------------------------------------------------------
#
#    META
#
# -----------------------------------------------------------------------------
class MetaViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        Provide Meta data about Stories
        """
        stories = Story.objects.public()
        meta    =  {}
        meta.update(stories.aggregate(Max('current_value_usd'), Min('current_value_usd')))
        meta['count'] = stories.count()
        return Response(meta)

# -----------------------------------------------------------------------------
#
#    FILTERS (which return results)
#
# -----------------------------------------------------------------------------
class FiltersViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        Provide countries, currencies and themes filters wich return results
        """
        filters = {
            "currency" : [],
            "theme"    : [],
            "country"  : []
        }
        # currencies
        currencies = Currency.objects.values("iso_code", "name")
        for currency in currencies:
            if Story.objects.public().filter(currency__iso_code=currency['iso_code']).count() > 0 :
                filters['currency'].append({"key":currency['iso_code'], 'value':currency['name']})
        # themes
        themes = Theme.objects.values("slug", "title")
        for theme in themes:
            if Story.objects.public().filter(themes__slug=theme['slug']).count() > 0 :
                filters['theme'].append({"key":theme['slug'], 'value':theme['title']})
        # countries
        for country in webapp.core.fields.COUNTRIES:
            if Story.objects.public().filter(country=country[0]).count() > 0 :
                filters['country'].append({"key":country[0], 'value':country[1]})
        return Response(filters)

# -----------------------------------------------------------------------------
#
#    COUNTRIES
#
# -----------------------------------------------------------------------------
import webapp.core.fields
class CountryViewSet(ChoicesViewSet):
    class Meta: 
        choices = webapp.core.fields.COUNTRIES
    def create_element(self, c):
        return {"iso_code": c[0], "name": c[1]}

# EOF
