#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 14-Aug-2013
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


from django.test import SimpleTestCase
from django.test.client import Client
from webapp.core.models import Story
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from operator import itemgetter
from pprint import pprint as pp
from relevance import Relevance
import random
import warnings

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
            'type'       : "discrete",
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
        TOLERENCE = 94
        count     = {}
        for x in range(100):
            relevance_for = random.randint(1,200) * int("1" + "0" * random.randint(1,15))
            if relevance_for in count:
                continue
            count[relevance_for] = 0
            response = self.client.get("/api/stories-nested/?relevance_for=%s" % (relevance_for))
            self.assertEquals(response.status_code, 200)
            assert len(response.data) > 0
            for story in response.data:
                # we check all attribute that should be presents 
                self.assertIsNotNone(story['relevance_score'])
                self.assertIsNotNone(story['relevance_type' ])      
                
                self.assertIsNotNone(story['relevance_ratio'])
                self.assertIsNotNone(story['relevance_value'])
                
                relevance_type = story['relevance_type' ]

                self.assertFalse(relevance_type is Relevance.RELEVANCE_TYPE_NONE)
                count[relevance_for] += 1
                if story['type'] is 'over_one_year':
                    accepted_types = (
                        Relevance.RELEVANCE_TYPE_TIME, 
                        Relevance.RELEVANCE_TYPE_MULTIPLE, 
                        Relevance.RELEVANCE_TYPE_EQUIVALENT,
                        Relevance.RELEVANCE_TYPE_HALF,
                    )
                    self.assertTrue(relevance_type in accepted_types)


                if relevance_type is Relevance.RELEVANCE_TYPE_TIME:
                    # we will check time equivalence
                    value = story['relevance_value']
                    story_day_value = story['current_value_usd'] / 360

                    self.assertIsNotNone(value['months'])
                    self.assertIsNotNone(value['weeks'])
                    self.assertIsNotNone(value['days'])

                    reverse_ratio     = story['relevance_ratio'] * story['current_value_usd'] 
                    reverse_computing = (value['months'] * 30 + value['weeks'] * 7 + value['days']) * story_day_value

                    accuracy = min(reverse_computing, relevance_for) / max(reverse_computing, relevance_for) * 100

                    debug = "\n"
                    debug += "\n{0:20}: {1}"          .format('user query'       , relevance_for)
                    debug += "\n{0:20}: {1} (id: {2})".format('story value'      , story['current_value_usd'], story['id'])
                    debug += "\n{0:20}: {1}"          .format('relevance_score'  , story['relevance_score'])
                    debug += "\n{0:20}: {1}"          .format('relevance_type'   , story['relevance_type'])
                    debug += "\n{0:20}: {1}"          .format('relevance_value'  , story['relevance_value'])
                    debug += "\n{0:20}: {1}"          .format("relevance_ratio"  , story['relevance_ratio'])
                    debug += "\n{0:20}: {1}"          .format("day value"        , story_day_value)
                    debug += "\n{0:20}: {1}"          .format("reverse_computing", reverse_computing)
                    debug += "\n{0:20}: {1}%"         .format("accuracy"         , accuracy)
                    debug += "\n--------------------------------------"
                    if accuracy < TOLERENCE:
                        warnings.warn("time equivalence accurency under %s%%: %s" % (TOLERENCE, debug))

                elif relevance_type in (Relevance.RELEVANCE_TYPE_PERCENTAGE, Relevance.RELEVANCE_TYPE_HALF, Relevance.RELEVANCE_TYPE_MULTIPLE):
                    
                    ratio_gap = abs(story['relevance_ratio'] - story['relevance_value'])
                    print "ratio gap: %f, ratio: %f, value: %f" % (ratio_gap, ratio, value)  
                    self.assertTrue( ratio_gap <= 0.05)

                

                if story['relevance_score'] > 8:
                    
                    if story['relevance_type'] in (Relevance.RELEVANCE_TYPE_MULTIPLE, Relevance.RELEVANCE_TYPE_HALF) :
                        reverse_computing = float(story['relevance_value']) * story['current_value_usd']
                        accuracy = min(reverse_computing, relevance_for) / max(reverse_computing, relevance_for) * 100
                        debug = "\n"
                        debug += "\n{0:20}: {1}"          .format('user query'       , relevance_for)
                        debug += "\n{0:20}: {1} (id: {2})".format('story value'      , story['current_value_usd'], story['id'])
                        debug += "\n{0:20}: {1}"          .format('relevance_score'  , story['relevance_score'])
                        debug += "\n{0:20}: {1}"          .format('relevance_type'   , story['relevance_type'])
                        debug += "\n{0:20}: {1}"          .format('relevance_value'  , story['relevance_value'])
                        debug += "\n{0:20}: {1}"          .format("reverse_computing", reverse_computing)
                        debug += "\n{0:20}: {1}%"         .format("accuracy"         , accuracy)
                        debug += "\n--------------------------------------"
                        if accuracy < TOLERENCE:
                            warnings.warn("accurency under %s%%: %s" % (TOLERENCE, debug))
        count = sorted(count.iteritems(), key=itemgetter(1), reverse=True)
        # pp(count[:5])

# EOF
