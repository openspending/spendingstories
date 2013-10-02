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
# Last mod : 21-Aug-2013
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

    def __nice_multiple_for(self, ratio):
        """ x200, x500, x1000. For instance: the query is twice the amount """
        nice_multiple = False
        ratio_rounded = round(ratio)
        relevance     = 6
        for i in range(1, 10):
            # we try to find with 4 percent of tolerance the nearest factor
            # as <factor> * <value> = relevance_for  
            hundred_mult = i * 100
            tolerance = 4
            nice_range = range(hundred_mult-tolerance, hundred_mult+tolerance)
            if ratio_rounded in nice_range:
                nice_multiple = i
        if not nice_multiple:
            nice_multiple =  round(ratio_rounded / 100, 1)

        if nice_multiple in [2, 5, 10]:
            relevance = 8
        elif nice_multiple in range(3, 9):
            relevance = 7
        if nice_multiple > 10:
            relevance = 5
        return Relevance(
            relevance, Relevance.RELEVANCE_TYPE_MULTIPLE, nice_multiple, ratio / 100
        )


    def __nice_equivalence(self, amount, compared_to):
        """ ratio equivalence if it's 50% """ 
        ratio = amount/compared_to * 100
        relevance = None
        original_ratio = ratio / 100
        if 90 <= ratio <= 110:
            relevance =  Relevance(10, Relevance.RELEVANCE_TYPE_EQUIVALENT, 1, original_ratio)
        elif 49 < ratio < 51:
            relevance =  Relevance(9, Relevance.RELEVANCE_TYPE_HALF, 0.5, original_ratio)
        elif ratio > 100:
            relevance = self.__nice_multiple_for(ratio)
        else:
            relevance = Relevance(0, Relevance.RELEVANCE_TYPE_NONE, None, original_ratio)
        return relevance

    def supertypes(self):
        return (
            Relevance.RELEVANCE_TYPE_EQUIVALENT, 
            Relevance.RELEVANCE_TYPE_MULTIPLE,
            Relevance.RELEVANCE_TYPE_HALF
        )




# EOF
