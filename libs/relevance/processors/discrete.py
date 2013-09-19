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

from relevance import Relevance, Processor
import math

class SubProcessor(Processor):

    def compute(self, amount, compared_to, *args, **kwargs):
        """ compute the relevance for a discrete reference """
        relevance = super(SubProcessor, self).compute(amount, compared_to, *args, **kwargs)
        ratio = amount/compared_to * 100

        if not relevance.type in self.supertypes():
            # if it has not been yet processed as: equivalent, half or multiple
            relevance.type  = Relevance.RELEVANCE_TYPE_PERCENTAGE
            if relevance.type is Relevance.RELEVANCE_TYPE_HALF:
                relevance.value = 0.5
            else:
                rounded_ratio = round(ratio)
                if ratio > 1:
                    if  rounded_ratio % 10 == 0:
                        relevance.score = 8
                    elif rounded_ratio % 5 == 0:
                        relevance.score = 7
                else:
                    relevance.score = 6

                relevance.value = rounded_ratio/100
        return relevance
# EOF
