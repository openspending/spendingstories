#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 06-Aug-2013
# Last mod : 06-Aug-2013
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

from economics import Inflation, CPI
import datetime
import os

# -----------------------------------------------------------------------------
#
#    INFLATION
#
# -----------------------------------------------------------------------------
# Load in memory the datapackage on launching, pretty faster
CPI       = CPI(datapackage=os.path.join((os.path.dirname(os.path.realpath(__file__))), "..", "data/cpi/"))
INFLATION = Inflation(CPI)
INFLATION_REFERENCE_RETRY = 5

def get_inflation(amount, year, country):
	def closest_ajustment_reference_date():
	    cpi_closest = CPI.closest(
	        country = country,
	        date    = datetime.date.today(),
	        limit   = datetime.timedelta(366*5))
	    return cpi_closest.date
	_year = year
	for i in range(INFLATION_REFERENCE_RETRY):
		reference_date = closest_ajustment_reference_date()
		try:
			return (INFLATION.inflate(amount, reference_date, datetime.date(_year, 1, 1), country),
				reference_date.year )
		except KeyError:
			_year = _year - 1
	raise Exception("no date found for inflation. Asked for %s and tested up to %s (%s)" % (year, _year + 1, country))

# EOF
