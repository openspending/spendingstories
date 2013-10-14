#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 21-Aug-2013
# Last mod : 11-Oct-2013
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

from relevance import Relevance

class Processor(object):
    """ Base class to compute a relevance """

    def compute(self, amount, compared_to, *args, **kwargs):
        """ Should be implemented and return a Relevance instance """
        return self.__nice_equivalence(amount, compared_to)

    def __nice_equivalence(self, amount, compared_to):
        ratio = amount/compared_to * 100
        relevance = None
        if 90 <= ratio <= 110:
            relevance =  Relevance(10, Relevance.RELEVANCE_TYPE_EQUIVALENT, 1)
        elif 49 < ratio < 51:
            relevance =  Relevance(9, Relevance.RELEVANCE_TYPE_HALF, 0.5)
        elif ratio > 100:
            # x200, x500, x1000. For instance: the query is twice the amount
            nice_multiple = False
            ratio_rounded = round(ratio)
            relevance_score     = 6
            for i in range(1, 10):
                # we try to find with 4 percent of tolerance the nearest factor
                # as <factor> * <value> = relevance_for  
                hundred_mult = i * 100
                tolerance = 4
                nice_range = range(hundred_mult-tolerance, hundred_mult+tolerance)
                if ratio_rounded in nice_range:
                    nice_multiple = i
                    break
            if nice_multiple:
                if nice_multiple in [2, 5, 10]:
                    relevance_score = 8
                elif nice_multiple in range(3, 9):
                    relevance_score = 7
                elif nice_multiple > 10:
                    relevance_score = 5
                relevance = Relevance(relevance_score, Relevance.RELEVANCE_TYPE_MULTIPLE, nice_multiple)
        return relevance

# EOF
