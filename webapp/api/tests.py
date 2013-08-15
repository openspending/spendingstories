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

    # def test_api_story_create(self):
    #     YEARS     = range(2003, 2013)
    #     CURRENCY  = Currency.objects.all()
    #     THEMES    = list(Theme.objects.public())

    #     for i in range(20):
    #         story = {}
    #         story['title']       = loremipsum.generate_sentence()[2].rstrip(".")
    #         story['description'] = random.choice( [loremipsum.generate_sentence()[2].rstrip("."),"", None] )
    #         story['value']       = random.randint(1,200) * int("1" + "0" * random.randint(1,15))
    #         story['year']        = random.choice(YEARS)
    #         story['country']     = random.choice(COUNTRIES)[0]
    #         story['currency']    = random.choice(CURRENCY).pk
    #         story['status']      = random.choice(('published', 'refused', 'pending'))
    #         story['continuous']  = random.randint(0,1) == 0
    #         story['source']      = "http://www.okf.org"
    #         story['sticky']      = random.randint(0,1) == 0
    #         story['themes']      = []
    #         for i in range(0, random.randint(1,4)):
    #             story['themes'].append(random.choice(THEMES).pk)

    #         response = self.staff_client.post('/api/stories/', story)
    #         self.assertEquals(response.status_code, 201, response)
    #         self.assertNotEquals(response.data['inflation_last_year'], "")
    #         self.assertNotEquals(response.data['current_value_usd']  , "")
    #         self.assertNotEquals(response.data['current_value']      , "")


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
