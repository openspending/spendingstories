#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 16-Aug-2013
# Last mod : 16-Aug-2013
# -----------------------------------------------------------------------------
"""

SPENDING STORIES sub module

* Compute a grade of relevance to an amount based on a reference.

* Support two types of reference: discrete and continuous values
    Discrete is an amount fixed, timeless. Continous represents more a buget, an annual cost.

For more informations, see https://github.com/jplusplus/okf-spending-stories/wiki/The-cards-visualization

"""

__version__ = '0.5'

class Relevance:
    """

    How to use it
    -------------

        score, type, value = Relevance(
            amount      = 10000,
            compared_to = 1234567890e+2,
            discrete    = True).values()

    * or *

        relevance = Relevance(
            amount      = 10000,
            compared_to = 1234567890e+2,
            discrete    = True)
        score = relevance.score
        type  = relevance.type
        value = relevance.value

    * or *

        relevance = Relevance(
            compared_to = 1234567890e+2,
            discrete    = True)
        relevance.compute(amount=10000)
        score, type, value = relevance.values()

    """

    # CONSTANTES
    TYPE_HALF       = "half"
    TYPE_EQUIVALENT = "equivalent"
    TYPE_MULTIPLE   = "multiple"
    TYPE_WEEK       = "weeks"
    TYPE_MONTH      = "months"

    def __init__(self, amount=None, compared_to=None, discrete=True):
        self.score = None
        self.value = None
        self._amount      = amount
        self._compared_to = compared_to
        if amount and compared_to:
            self.compute(amount, compared_to, discrete)

    def compute(self, amount=None, compared_to=None, discrete=True):
        """ choose the right method related to the nature of the reference (discrete or continuous) """
        amount      = amount      or self._amount
        compared_to = compared_to or self._compared_to
        if discrete:
            self.__compute_discrete_relevance(float(amount), float(compared_to))
        else:
            self.__compute_continuous_relevance(float(amount), float(compared_to))
        return self

    def __compute_discrete_relevance(self, amount, compared_to):
        """ compute the relevance for a discrete reference """
        ratio = amount/compared_to * 100
        if 90 <= ratio <= 110:
            return self.__set_values(10, Relevance.TYPE_EQUIVALENT)
        else:
            if ratio < 100:
                if not ratio < 1:
                    if 49 < ratio < 51:
                        # near
                        return self.__set_values(9, Relevance.TYPE_HALF, 0.5)
                    else:
                        if round(ratio) % 10 == 0:
                            # multiple of 10
                            return self.__set_values(8, Relevance.TYPE_MULTIPLE, round(ratio)/100)
            else:
                if ratio < 1002:
                    # x200, x500, x1000. For instance: the query is twice the amount
                    nice_multiple = self.__nice_multiple_for(ratio)
                    if nice_multiple:
                        return self.__set_values(8, Relevance.TYPE_MULTIPLE, nice_multiple)
        return self.__set_values(0)

    def __compute_continuous_relevance(self, amount, compared_to):
        """ compute the relevance for a continuous reference """
        ratio = amount/compared_to * 100
        if 90 <= ratio <= 110:
            return self.__set_values(10, Relevance.TYPE_EQUIVALENT)
        else:
            if ratio < 100:
                if 49 < ratio < 51:
                    return self.__set_values(9, Relevance.TYPE_HALF, 0.5)
                else:
                    # compute the story amount equivalence for 1 day
                    one_day   = compared_to / 365.25
                    one_week  = compared_to / 52
                    one_month = compared_to / 12
                    if amount < one_month:
                        # compute into weeks
                        if amount >= one_week and amount % one_week <= one_day * 0.25:
                            return self.__set_values(8, Relevance.TYPE_WEEK, int(amount / one_week))
                    elif amount < compared_to:
                        # compute into month
                        if amount % one_month < one_week * 0.25:
                            return self.__set_values(8, Relevance.TYPE_MONTH, int(amount / one_month))
            else:
                if ratio < 1002:
                    # x200, x500, x1000. For instance: the query is twice the amount
                    nice_multiple = self.__nice_multiple_for(ratio)
                    if nice_multiple:
                        return self.__set_values(8, Relevance.TYPE_MULTIPLE, nice_multiple)
        return self.__set_values(0)

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

    def __set_values(self, score, _type=None, value=None):
        self.score = score
        self.type  = _type
        self.value = value

    def values(self):
        """ return the score and the value as a tuple """
        return (self.score, self.type, self.value)

# EOF
