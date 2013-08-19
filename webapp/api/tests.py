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
# Last mod : 16-Aug-2013
# -----------------------------------------------------------------------------

from django.test import SimpleTestCase
from django.test.client import Client
from webapp.core.models import Story
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from operator import itemgetter
from pprint import pprint as pp
import random

class APIStoryTestCase(SimpleTestCase):
    def setUp(self):
        # Every test needs a client.
        staff_token, created = Token.objects.get_or_create(user=User.objects.filter(is_staff=True)[0])
        self.staff_client    = Client(HTTP_AUTHORIZATION="Token %s" % staff_token.key)
        self.client          = Client()

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

    def test_api_relevances(self):
        count = {}
        for x in range(10):
            relevance_for = random.randint(1,200) * int("1" + "0" * random.randint(1,15))
            if relevance_for in count:
                continue
            count[relevance_for] = 0
            response = self.client.get("/api/stories-nested/?relevance_for=%s" % (relevance_for))
            self.assertEquals(response.status_code, 200)
            assert len(response.data) > 0
            for story in response.data:
                self.assertIsNotNone(story['relevance_score'])
                if story['relevance_score'] != 0:
                    count[relevance_for] += 1
                    # print story['relevance_score'], story['relevance_type'], story['relevance_value']
        count = sorted(count.iteritems(), key=itemgetter(1), reverse=True)
        # pp(count[:5])

    def test_api_relevance(self):
        relevance_for = 530000000
        response = self.client.get("/api/stories-nested/?relevance_for=%s" % (relevance_for))
        self.assertEquals(response.status_code, 200)
        assert len(response.data) > 0
        for story in response.data:
            self.assertIsNotNone(story['relevance_score'])
            self.assertTrue('relevance_value' in story)
            # if story['relevance_score'] > 0:
            #     print 
            #     print "{0:12}: {1}"          .format('user query' , relevance_for)
            #     print "{0:12}: {1} (id: {2})".format('story value', story['current_value_usd'], story['id'])
            #     print "{0:12}: {1}"          .format('score'      , story['relevance_score'])
            #     print "{0:12}: {1}"          .format('type'       , story['relevance_type'])
            #     print "{0:12}: {1}"          .format('value'      , story['relevance_value'])
            #     print "--------------------------------------"

# EOF
