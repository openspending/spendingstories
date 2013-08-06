#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 05-Aug-2013
# Last mod : 05-Aug-2013
# -----------------------------------------------------------------------------

from django.utils.translation import ugettext as _
from webapp.currency.models import Currency
from django.db import models
import fields
import datetime
import utils 


YEAR_CHOICES = []
for r in range(1999, (datetime.datetime.now().year)):
    YEAR_CHOICES.append((r,r))

# -----------------------------------------------------------------------------
#
#    THEMES
#
# -----------------------------------------------------------------------------
class Theme(models.Model):
    title       = models.CharField(max_length=80)
    slug        = models.SlugField(primary_key=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.title

# -----------------------------------------------------------------------------
#
#    STORY
#
# -----------------------------------------------------------------------------
class Story(models.Model):
    '''
    The model representing a spending
    '''
    created_at         = models.DateTimeField(auto_now_add=True, editable=False)
    value              = models.IntegerField(_('The spending value')) # The spending amount
    current_value_usd  = models.IntegerField(_('Current value in USD'), editable=False) # The spending amount
    title              = models.CharField(_('Story title'), max_length=140)
    country            = fields.CountryField() # ISO code of the country 
    source             = models.URLField(_('Story\'s source URL'), null=True, blank=True, max_length=140)
    currency           = models.ForeignKey(Currency)
    continuous         = models.BooleanField(_('Is a countinuous spending'), default=False)
    published          = models.BooleanField(_('Publish this story'),        default=False)
    sticky             = models.BooleanField(_('Is a top story'),            default=False)
    year               = models.IntegerField(_('The spending year'),         choices=YEAR_CHOICES)
    themes             = models.ManyToManyField(Theme)

    def __unicode__(self):
        return self.title

    def _inflate_value(self):
        '''
        Used to ajust the value of the story value
        '''
        return utils.get_inflation(amount=self.value, year=self.year, country=self.country)

    current_value = property(_inflate_value)

    def save(self):
        '''
        save in database
        '''
        try:
            previous_instance = Story.objects.get(pk=self.pk)
        except:
            previous_instance = None
        # if current_value or currency have changed, recompute the current_value_usd
        if not self.current_value_usd \
        or previous_instance.currency      != self.currency \
        or previous_instance.current_value != self.current_value:
            self.current_value_usd = self.current_value / self.currency.rate
        super(Story, self).save()

# EOF
