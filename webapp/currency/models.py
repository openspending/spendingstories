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
from django.db import models

class Currency(models.Model):
    iso_code = models.CharField(primary_key=True, max_length=3)
    name     = models.CharField(max_length=120)
    rate     = models.FloatField()

    def __unicode__(self):
        return "%s - %s" % (self.name, self.iso_code)

# EOF
