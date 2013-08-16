#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 14-Aug-2013
# Last mod : 15-Aug-2013
# -----------------------------------------------------------------------------

from django.test import TestCase
from django.test.client import Client
from webapp.core.models import Story
from webapp.core.models import Theme
from webapp.currency.models import Currency
from webapp.core.fields import COUNTRIES
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import random
import loremipsum

class APIStoryTestCase(TestCase):
    def setUp(self):
        # Every test needs a client.
        staff_token = Token.objects.create(user=User.objects.filter(is_staff=True)[0])
        self.staff_client = Client(HTTP_AUTHORIZATION="Token %s" % staff_token.key)
        self.client       = Client()

    def test_api_story_list(self):
        response = self.client.get('/api/stories/')
        self.assertEquals(response.status_code, 200, response)
        assert len(response.data) > 0
        for story in response.data:
            assert story['status'] == 'published', "This story souldn't be there: %s" % story

    def test_api_story_retrieve(self):
        story    = Story.objects.public()[0]
        response = self.client.get('/api/stories/%s/' % story.pk)
        self.assertEquals(response.status_code, 200, response)

    def test_api_story_nested_list(self):
        response = self.client.get('/api/stories-nested/')
        self.assertEquals(response.status_code, 200, response)
        assert len(response.data) > 0
        for story in response.data:
            assert story['status'] == 'published', "This story souldn't be there: %s" % story

    def test_api_story_nested_retrieve(self):
        story    = Story.objects.public()[0]
        response = self.client.get('/api/stories-nested/%s/' % story.pk)
        self.assertEquals(response.status_code, 200, response)

    def test_api_permissions(self):
        """
        PERMISSIONS TESTED :
            [ ]  staff        POST
            [ ]  no-auth      POST
            [ ]  regular user POST
        """
        story = {
            'continuous' : False,
            'country'    : 'BGR',
            'currency'   : u'GNF',
            'description': None,
            'source'     : 'http://www.okf.org',
            'status'     : 'published',
            'sticky'     : True,
            'themes'     : [],
            'title'      : 'Velit ipsum augue',
            'value'      : 1420000,
            'year'       : 2003}
        # staff
        response = self.staff_client.post('/api/stories/', story)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['status'], 'published')
        self.assertEquals(response.data['sticky'], True)
        # no-auth
        response = self.client.post('/api/stories/', story)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['status'], 'pending')
        self.assertEquals(response.data['sticky'], False)
        # regular user
        user, created = User.objects.get_or_create(username="pouet", email="pouet@pouet.org")
        regular_token, created = Token.objects.get_or_create(user=user)
        self.regular_client    = Client(HTTP_AUTHORIZATION="Token %s" % regular_token.key)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['status'], 'pending')
        self.assertEquals(response.data['sticky'], False)

# EOF
