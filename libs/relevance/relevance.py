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

For more informations, see https://github.com/jplusplus/okf-spending-stories/wiki/The-cards-visualization

"""

__version__ = '0.6'

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
    # STORIES_TYPES = ("discrete", "over_one_year", "per_population")
    # output
    RELEVANCE_TYPE_HALF       = "half"
    RELEVANCE_TYPE_EQUIVALENT = "equivalent"
    RELEVANCE_TYPE_MULTIPLE   = "multiple"
    RELEVANCE_TYPE_WEEK       = "weeks"
    RELEVANCE_TYPE_MONTH      = "months"

    def __init__(self, score=None, relevance_type=None, value=None):
        self.score = score
        self.value = relevance_type
        self.type  = value

    def compute(self, amount, compared_to, story_type):
        """ choose the right method related to the nature of the reference (discrete or over_one_year) """
        # FIXME
        # if story_type in Relevance.STORIES_TYPES:
        import processors
        processor = eval("processors.%s.Processor()" % story_type)
        self.__set_values(*processor.compute(float(amount), float(compared_to)).values())
        return self.values()

    def values(self):
        """ return the score and the value as a tuple """
        return (self.score, self.type, self.value)

    def __set_values(self, score, relevance_type=None, value=None):
        self.score = score
        self.type  = relevance_type
        self.value = value

class Processor:

    def compute(self, amount, compared_to, *args, **kwargs):
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
