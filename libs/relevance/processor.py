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

class Processor:
    """ Base class to compute a relevance """

    def compute(self, amount, compared_to, *args, **kwargs):
        """ Should be implemented and return a Relevance instance """
        raise Exception("do be implemented")

    def __nice_multiple_for(self, ratio):
        """ x200, x500, x1000. For instance: the query is twice the amount """
        nice_multiple = False
        ratio_rounded = round(ratio)
        if ratio_rounded in range(198, 202):
            nice_multiple = 2
        elif ratio_rounded in range(498, 502):
            nice_multiple = 5
        elif ratio_rounded in range(996, 1002):
            nice_multiple = 10
        return nice_multiple

# EOF
