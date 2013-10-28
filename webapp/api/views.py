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
# Last mod : 07-Oct-2013
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

from webapp.core.models      import Story, Theme, Page
from webapp.currency.models  import Currency
from rest_framework          import viewsets
from rest_framework          import filters
from rest_framework.response import Response
from rest_framework          import permissions
from django.db.models        import Max, Min, Q
from relevance               import Relevance
from viewsets                import ChoicesViewSet

import webapp.core.fields
import serializers
# -----------------------------------------------------------------------------
#
#    STORIES
#
# -----------------------------------------------------------------------------
class StoryPermission(permissions.BasePermission):
    """
    Permissions for Stories
    """
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
    Results can be filtered using the following fields:
    
    ### Filter fields 

    - **sticky** &nbsp; `Boolean`  <br/>

        Will filter stories based on their `sticky` attribute (Sticky stories are tabloid stories selected by administrators).<br/>
        *Possible values:* `True`, `False`, `''` *(empty is understood as True)*<br/>
    
    - **country** &nbsp; `String`  <br/>

        Will filter stories based on the given country<br/>
        *Possible values:* The iso code of the wanted country, see [/api/countries/](/api/countries/) for more details.

    
    - **currency** &nbsp; `String`  <br/>
        
        Will filter stories based on the given currency<br/>
        *Possible values:* The iso code of the wanted currency, see [/api/currencies/](/api/currencies/) for more details.
    
    - **type** &nbsp; `String`  <br/>
        
        Will filter stories based on their type.<br/>
        *Possible values:* `over_one_year`, `discrete`, see [the wiki page](/api/currencies/) for more details.


    - **title** &nbsp; `String`  <br/>

        Will filter stories based on their title.<br/>

    
    - **themes** &nbsp; `String`  - *stackable* <br/>
    
        Will filter stories based on their theme(s).<br/>
        > **Note:** this attribute is stackable. This means you can add multiple times the same attribute to the URL.<br/>
        > `GET /api/stories/?themes=aid&themes=health` will return all stories having `aid` **OR** `health` in their themes 



    """
    queryset           = Story.objects.public()
    serializer_class   = serializers.StorySerializer
    filter_fields      = ('sticky', 'country', 'currency','type', 'title', 'themes')
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (StoryPermission,)

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
                score, _type, value = Relevance().compute(
                    amount      = relevance_for,
                    compared_to = story['current_value_usd'],
                    story_type  = story['type'])
                story['relevance_score'] = score
                story['relevance_type' ] = _type
                story['relevance_value'] = value
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
class CountryViewSet(ChoicesViewSet):
    class Meta: 
        choices = webapp.core.fields.COUNTRIES
    def create_element(self, c):
        return {"iso_code": c[0], "name": c[1]}

# -----------------------------------------------------------------------------
#
#    PAGES
#
# -----------------------------------------------------------------------------
class PagesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = serializers.PageSerializer
    filter_fields      = ('slug',)

# EOF
