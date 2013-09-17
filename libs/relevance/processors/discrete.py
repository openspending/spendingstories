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

class Processor(Processor):

    def compute(self, amount, compared_to, *args, **kwargs):
        """ compute the relevance for a discrete reference """
        ratio = amount/compared_to * 100
        if 90 <= ratio <= 110:
            return Relevance(10, Relevance.RELEVANCE_TYPE_EQUIVALENT)
        else:
            if ratio < 100:
                percentage = ratio / 100
                relevance_value = round(ratio) / 100 

                relevance  = 6
                relevance_type = Relevance.RELEVANCE_TYPE_PERCENTAGE
                if not ratio < 1:
                    if 49 < ratio < 51:
                        relevance       = 9
                        relevance_type  = Relevance.RELEVANCE_TYPE_HALF
                        relevance_value = 0.5
                    else:
                        if round(ratio) % 10 == 0:
                            relevance = 8
                        elif round(ratio) % 5 == 0:
                            relevance = 7
                else:
                    relevance = 5
                    relevance_type = Relevance.RELEVANCE_TYPE_PERCENTAGE
                return Relevance(relevance, relevance_type, relevance_value)
            else:
                return self.__nice_multiple_for(ratio)
        return Relevance(0)

# EOF
