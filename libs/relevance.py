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
            compared_to = 50000,
            story_type  = "discrete").values()

    * or *

        relevance = Relevance(
            amount      = 10000,
            compared_to = 1234567890e+2,
            story_type  = "discrete")
        score = relevance.score
        type  = relevance.type
        value = relevance.value

    * or *

        relevance = Relevance(
            compared_to = 1234567890e+2,
            story_type  = "discrete")
        relevance.compute(amount=10000)
        score, type, value = relevance.values()

    """

    # CONSTANTES
    # input
    # STORIES_TYPE_DISCRETE     = "discrete"
    # STORIES_TYPE_CONTINUOUS   = "continuous"
    STORIES_TYPES = ("discrete", "continuous")
    # output
    RELEVANCE_TYPE_HALF       = "half"
    RELEVANCE_TYPE_EQUIVALENT = "equivalent"
    RELEVANCE_TYPE_MULTIPLE   = "multiple"
    RELEVANCE_TYPE_WEEK       = "weeks"
    RELEVANCE_TYPE_MONTH      = "months"

    def __init__(self, amount=None, compared_to=None, story_type=None):
        self.score = None
        self.value = None
        self._amount      = amount
        self._compared_to = compared_to
        self._story_type   = story_type
        if self._amount and self._compared_to and self._story_type:
            self.compute()

    def compute(self, amount=None, compared_to=None, story_type=None):
        """ choose the right method related to the nature of the reference (discrete or continuous) """
        amount      = amount      or self._amount
        compared_to = compared_to or self._compared_to
        story_type  = story_type  or self._story_type
        assert amount and compared_to and story_type
        if story_type in Relevance.STORIES_TYPES:
            getattr(self, "_compute_%s_relevance" % story_type)(float(amount), float(compared_to))
        # if discrete:
        #     self.__compute_discrete_relevance(float(amount), float(compared_to))
        # else:
        #     self.__compute_continuous_relevance(float(amount), float(compared_to))
        return self

    def _compute_discrete_relevance(self, amount, compared_to):
        """ compute the relevance for a discrete reference """
        ratio = amount/compared_to * 100
        if 90 <= ratio <= 110:
            return self.__set_values(10, Relevance.RELEVANCE_TYPE_EQUIVALENT)
        else:
            if ratio < 100:
                if not ratio < 1:
                    if 49 < ratio < 51:
                        # near
                        return self.__set_values(9, Relevance.RELEVANCE_TYPE_HALF, 0.5)
                    else:
                        if round(ratio) % 10 == 0:
                            # multiple of 10
                            return self.__set_values(8, Relevance.RELEVANCE_TYPE_MULTIPLE, round(ratio)/100)
            else:
                if ratio < 1002:
                    # x200, x500, x1000. For instance: the query is twice the amount
                    nice_multiple = self.__nice_multiple_for(ratio)
                    if nice_multiple:
                        return self.__set_values(8, Relevance.RELEVANCE_TYPE_MULTIPLE, nice_multiple)
        return self.__set_values(0)

    def _compute_continuous_relevance(self, amount, compared_to):
        """ compute the relevance for a continuous reference """
        ratio = amount/compared_to * 100
        if 90 <= ratio <= 110:
            return self.__set_values(10, Relevance.RELEVANCE_TYPE_EQUIVALENT)
        else:
            if ratio < 100:
                if 49 < ratio < 51:
                    return self.__set_values(9, Relevance.RELEVANCE_TYPE_HALF, 0.5)
                else:
                    # compute the story amount equivalence for 1 day
                    one_day   = compared_to / 365.25
                    one_week  = compared_to / 52
                    one_month = compared_to / 12
                    if amount < one_month:
                        # compute into weeks
                        if amount >= one_week and amount % one_week <= one_day * 0.25:
                            return self.__set_values(8, Relevance.RELEVANCE_TYPE_WEEK, int(amount / one_week))
                    elif amount < compared_to:
                        # compute into month
                        if amount % one_month < one_week * 0.25:
                            return self.__set_values(8, Relevance.RELEVANCE_TYPE_MONTH, int(amount / one_month))
            else:
                if ratio < 1002:
                    # x200, x500, x1000. For instance: the query is twice the amount
                    nice_multiple = self.__nice_multiple_for(ratio)
                    if nice_multiple:
                        return self.__set_values(8, Relevance.RELEVANCE_TYPE_MULTIPLE, nice_multiple)
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

    def __set_values(self, score, relevance_type=None, value=None):
        self.score = score
        self.type  = relevance_type
        self.value = value

    def values(self):
        """ return the score and the value as a tuple """
        return (self.score, self.type, self.value)

# EOF
