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

from relevance import Processor, Relevance
import math

class SubProcessor(Processor):

    def compute(self, amount, compared_to, *args, **kwargs):
        """ compute the relevance for an over_one_year reference """
        relevance = super(SubProcessor, self).compute(amount, compared_to, *args, **kwargs)
        time_equivalence =  Relevance.RELEVANCE_TYPE_TIME
        if not relevance.type in self.supertypes():
            # if it has not been yet processed as: equivalent, half or multiple
            relevance.type = time_equivalence
            equivalence    = self._compute_value(amount, compared_to)

            nb_months = equivalence['months']
            nb_weeks  = equivalence['weeks']
            nb_days   = equivalence['days']

            if nb_months == 0:
                if nb_weeks == 0:
                    if nb_days > 0:
                        relevance.score = 7
                    else:
                        relevance.score = 6
                else: 
                    if nb_days <= 1:
                        relevance.score = 8
                    else:
                        relevance.score = 6
            else: 
                if nb_weeks == 0 and nb_days <= 1:
                    relevance.score = 8
                else:
                    if nb_days <= 1:
                        relevance.score = 7
                    else:
                        relevance.score = 6

            relevance.value = equivalence
        return relevance

    def _compute_value(self, amount, compared_to):
        """
        This function assume amount < compared_to
        """ 
        assert(amount < compared_to)
        dict_values = {
            'months': 0,
            'weeks':  0,
            'days':   0
        }
        # compute the story amount equivalence for 1 day
        total_days  = 360
        months_days = total_days / 12
        weeks_days  = 7


        one_day   = compared_to / total_days
        total_nb_days  = amount / one_day
        if total_nb_days < 1:
            # in that case it's useless to compute a time equivalence
            weeks  = 0
            months = 0
            days   = 1 if total_nb_days > 0.9 else 0 
        else: 
            weeks  = math.floor((total_nb_days / weeks_days  ) % 4  )
            months = math.floor((total_nb_days / months_days ) % 12 )
            days   = math.floor(total_nb_days % 7)
       
        dict_values['weeks']  = weeks
        dict_values['months'] = months
        dict_values['days']   = days
        return dict_values


# EOF
