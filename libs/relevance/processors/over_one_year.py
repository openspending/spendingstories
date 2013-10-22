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

from relevance import Processor, Relevance

class SubProcessor(Processor):

    def compute(self, amount, compared_to, *args, **kwargs):
        """ compute the relevance for an over_one_year reference """
        relevance = super(SubProcessor, self).compute(amount, compared_to, *args, **kwargs)
        if not relevance and amount < compared_to:
            # compute the story amount equivalence for 1 day
            one_day   = compared_to / 365.25
            one_week  = compared_to / 52
            one_month = compared_to / 12
            if amount < one_week:
                if  amount > one_day and amount % one_day <= one_day * .1:
                    relevance = Relevance(6, Relevance.RELEVANCE_TYPE_DAY, int(amount / one_day))
            elif amount < one_month:
                # compute into weeks
                if amount >= one_week and amount % one_week <= one_day * 0.25:
                    relevance = Relevance(7, Relevance.RELEVANCE_TYPE_WEEK, int(amount / one_week))
            # compute into month
            elif amount % one_month < one_week * 0.25:
                relevance = Relevance(8, Relevance.RELEVANCE_TYPE_MONTH, int(amount / one_month))
        return relevance

# EOF
