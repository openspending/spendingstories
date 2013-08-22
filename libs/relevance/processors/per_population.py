#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 21-Aug-2013
# Last mod : 21-Aug-2013
# -----------------------------------------------------------------------------

from relevance import Processor, Relevance

class Processor(Processor):
    def compute(self, amount, compared_to, *args, **kwargs):
        ratio = amount/compared_to * 100
        if 90 <= ratio <= 110:
            return Relevance(10, Relevance.RELEVANCE_TYPE_EQUIVALENT)
        return Relevance(0)

# EOF
