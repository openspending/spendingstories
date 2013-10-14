#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 16-Aug-2013
# Last mod : 11-oct-2013
# -----------------------------------------------------------------------------
# This file is part of Spending Stories.
# 
#     Spending Stories is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Spending Stories is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Spending Stories.  If not, see <http://www.gnu.org/licenses/>.

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

    `amount` is the number that you want compute the relevance, related to `compated_to`.
    `story_type` is the nature of the `compared_to` value. It can take `discrete` (default value), `over_one_year` or other
    names of files in the `processors` package. This `story_type` will change the way that the relevance will be computed.

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
    RELEVANCE_TYPE_PERCENTAGE = "percentage"
    RELEVANCE_TYPE_WEEK       = "weeks"
    RELEVANCE_TYPE_MONTH      = "months"
    RELEVANCE_TYPE_DAY        = "days"

    def __init__(self, score=None, relevance_type=None, value=None):
        self.score = score
        self.value = value
        self.type  = relevance_type

    def compute(self, amount, compared_to, story_type="discrete", **extra_fields):
        """ choose the right processor related to the nature of the reference (discrete or over_one_year etc...) """
        import processors
        processor = eval("processors.%s.SubProcessor()" % story_type)
        relevance = processor.compute(float(amount), float(compared_to), **extra_fields)
        if relevance:
            self.__set_values(*relevance.values())
        else:
            self.__set_values(0)
        return self.values()

    def values(self):
        """ return the score and the value as a tuple """
        return (self.score, self.type, self.value)

    def __set_values(self, score, relevance_type=None, value=None):
        self.score = score
        self.type  = relevance_type
        self.value = value

# EOF
