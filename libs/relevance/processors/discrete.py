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

class Processor(Processor):

    def compute(self, amount, compared_to, *args, **kwargs):
        """ compute the relevance for a discrete reference """
        ratio = amount/compared_to * 100
        if 90 <= ratio <= 110:
            return Relevance(10, Relevance.RELEVANCE_TYPE_EQUIVALENT)
        else:
            if ratio < 100:
                if not ratio < 1:
                    if 49 < ratio < 51:
                        # near
                        return Relevance(9, Relevance.RELEVANCE_TYPE_HALF, 0.5)
                    else:
                        if round(ratio) % 10 == 0:
                            # multiple of 10
                            return Relevance(8, Relevance.RELEVANCE_TYPE_MULTIPLE, round(ratio)/100)
            else:
                if ratio < 1002:
                    # x200, x500, x1000. For instance: the query is twice the amount
                    nice_multiple = self.__nice_multiple_for(ratio)
                    if nice_multiple:
                        return Relevance(8, Relevance.RELEVANCE_TYPE_MULTIPLE, nice_multiple)
        return Relevance(0)

# EOF
