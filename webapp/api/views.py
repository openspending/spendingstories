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
# Last mod : 14-Aug-2013
# -----------------------------------------------------------------------------
from webapp.core.models import Story, Theme
from webapp.currency.models import Currency
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Max, Min
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
    filter_fields      = ('sticky', 'country', 'currency', 'themes', 'continuous')
    permission_classes = (StoryPermission,)

    def create(self, request, pk=None):
        # reset reserved field if not staff
        if not request.user or not request.user.is_staff:
            request.DATA['status'] = "pending"
            request.DATA['sticky'] = False
        response = super(StoryViewSet, self).create(request, pk)
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
        meta =  {}
        meta.update(Story.objects.public().aggregate(Max('current_value_usd'), Min('current_value_usd')))
        return Response(meta)

# EOF
