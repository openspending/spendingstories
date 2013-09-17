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
        """ compute the relevance for an over_one_year reference """
        ratio = amount/compared_to * 100
        if 90 <= ratio <= 110:
            return Relevance(10, Relevance.RELEVANCE_TYPE_EQUIVALENT)
        else:
            if ratio < 100:
                if 49 < ratio < 51:
                    return Relevance(9, Relevance.RELEVANCE_TYPE_HALF, 0.5)
                else:
                    # compute the story amount equivalence for 1 day
                    one_day   = compared_to / 365.25
                    one_week  = compared_to / 52
                    one_month = compared_to / 12
                    if amount < one_month:
                        # compute into weeks
                        if amount >= one_week and amount % one_week <= one_day * 0.25:
                            return Relevance(8, Relevance.RELEVANCE_TYPE_WEEK, int(amount / one_week))
                    elif amount < compared_to:
                        # compute into month
                        if amount % one_month < one_week * 0.25:
                            return Relevance(8, Relevance.RELEVANCE_TYPE_MONTH, int(amount / one_month))
            else:
                return self.__nice_multiple_for(ratio)
        return Relevance(0)

# EOF
