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
# Last mod : 21-Aug-2013
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

        score, type, value = Relevance().compute(
            amount      = 10000,
            compared_to = 50000,
            story_type  = "discrete")

    * or *

        relevance = Relevance()
        relevance.compute(
            amount      = 10000,
            compared_to = 50000,
            story_type  = "discrete")
        score = relevance.score
        type  = relevance.type
        value = relevance.value

    * or *

        relevance = Relevance()
        relevance.compute(
            amount      = 10000,
            compared_to = 50000,
            story_type  = "discrete")
        score, type, value = relevance.values()

    """

    # CONSTANTES
    RELEVANCE_TYPE_HALF       = "half"
    RELEVANCE_TYPE_EQUIVALENT = "equivalent"
    RELEVANCE_TYPE_MULTIPLE   = "multiple"
    RELEVANCE_TYPE_WEEK       = "weeks"
    RELEVANCE_TYPE_MONTH      = "months"

    def __init__(self, score=None, relevance_type=None, value=None):
        self.score = score
        self.value = value
        self.type  = relevance_type

    def compute(self, amount, compared_to, story_type, **extra_fields):
        """ choose the right processor related to the nature of the reference (discrete or over_one_year etc...) """
        import processors
        processor = eval("processors.%s.Processor()" % story_type)
        self.__set_values(*processor.compute(float(amount), float(compared_to), **extra_fields).values())
        return self.values()

    def values(self):
        """ return the score and the value as a tuple """
        return (self.score, self.type, self.value)

    def __set_values(self, score, relevance_type=None, value=None):
        self.score = score
        self.type  = relevance_type
        self.value = value

# EOF
