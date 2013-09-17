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
from relevance import Relevance

class Processor:
    """ Base class to compute a relevance """

    def compute(self, amount, compared_to, *args, **kwargs):
        """ Should be implemented and return a Relevance instance """
        raise Exception("do be implemented")

    def __nice_multiple_for(self, ratio):
        """ x200, x500, x1000. For instance: the query is twice the amount """
        nice_multiple = False
        ratio_rounded = round(ratio)
        relevance     = 6
        for i in range(1, 10):
            hundred_mult = i * 100
            tolerance = 10
            nice_range = range(hundred_mult-tolerance, hundred_mult+tolerance)
            if ratio_rounded in nice_range:
                nice_multiple = i
        if not nice_multiple:
            nice_multiple = round(ratio_rounded / 100, 2)

        if nice_multiple in [2, 5, 10]:
            relevance = 8
        elif nice_multiple in range(3, 9):
            relevance = 7
        if nice_multiple > 10:
            relevance = 5
        return Relevance(relevance, Relevance.RELEVANCE_TYPE_MULTIPLE, nice_multiple)

# EOF
