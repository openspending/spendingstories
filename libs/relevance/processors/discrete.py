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


from relevance import Relevance, Processor
import math

class SubProcessor(Processor):

    def compute(self, amount, compared_to, *args, **kwargs):
        """ compute the relevance for a discrete reference """
        relevance = super(SubProcessor, self).compute(amount, compared_to, *args, **kwargs)
        ratio = (amount/compared_to) * 100
        rounded_ratio = round(ratio)
        if not relevance.type in self.supertypes():
            # if it has not been yet processed as: equivalent, half or multiple
            if relevance.type is Relevance.RELEVANCE_TYPE_HALF:
                relevance.value = 0.5
            else:
                relevance.type  = Relevance.RELEVANCE_TYPE_PERCENTAGE
                if ratio > 1:
                    if   self.is_multiple_of(ratio, 10, 0.5):
                        relevance.score = 8
                    elif self.is_multiple_of(ratio, 5, 0.5):
                        relevance.score = 7
                    elif self.is_multiple_of(ratio, 1, 0.01):
                        relevance.score = 6
                    else:
                        relevance.score = 5
                else:
                    relevance.score = 5
                relevance.value = rounded_ratio / 100
        return relevance

    def is_multiple_of(self, n, m, tolerance):
        mod_nm   = n % m 
        return mod_nm == 0 or mod_nm <= tolerance or mod_nm >= (m - tolerance)
# EOF
