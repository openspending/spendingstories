#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : date
# Last mod : date
# -----------------------------------------------------------------------------
import random
import loremipsum
from webapp.core.models import Theme
from webapp.currency.models import Currency

YEARS    = range(1990, 2013)
CURRENCY = [_.iso_code for _ in Currency.objects.all()]
THEMES   = list(Theme.objects.all())

results  = []

for i in range(10):
    currency = random.choice(CURRENCY)
    year     = random.choice(YEARS)
    value    = random.randint(1,200) * int("1" + "0" * random.randint(1,15))
    rate     = Currency.objects.get(iso_code=currency).rate * value

    story = {
       "id"                  : i,
       "title"               : loremipsum.generate_sentence()[2].rstrip("."),
       "description"         : loremipsum.generate_sentence()[2].rstrip("."),
       "value"               : value,
       # "value_current"       : value_current,
       "value_usd_current"   : rate,
       "year"                : year,
       # "inflation_last_year" : inflation_last_year,
       "country"             : currency,
       "currency"            : currency,
       "continuous"          : random.randint(0,1) == 0,
       "source"              : "http://www.okf.org",
       "themes"              : random.choice(THEMES),
       "sticky"              : random.randint(0,1) == 0
    }
    results.append(story)

from pprint import pprint
pprint(results)

# EOF
