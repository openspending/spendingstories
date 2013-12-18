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

# -----------------------------------------------------------------------------
#
#    INFLATION
#
# -----------------------------------------------------------------------------
INFLATION_REFERENCE_RETRY = 5
CACHED_SOURCE_TIMEOUT = 1 # days
CACHED_SOURCE = None
CACHED_YEARS = None

def get_data():
	global CACHED_SOURCE
	# if cache exists and is less than 1 day
	if CACHED_SOURCE and (datetime.datetime.now() - CACHED_SOURCE[1]).days < CACHED_SOURCE_TIMEOUT :
		cpi = CACHED_SOURCE[0]
	else:
		cpi           = CPI()
		CACHED_SOURCE = (cpi, datetime.datetime.now())
	return cpi.data

def available_years():
	years = {}
	for key, value in get_data().items():
		years[key] = sorted(map(lambda _:_.year, value))
	return years

def get_inflation(amount, year, country):
	"""
	Get the inflated amount for the given year and country.
	Try to use the most recent date to compute the inflated amount.

	: param amount  : int
	: param year    : int
	: param country : ISO code, str
	: returns       : tuple((inflated_amount, most_recent_year_reference))
	"""
	global CACHED_SOURCE
	# if cache exists and is less than 1 day
	if CACHED_SOURCE and (datetime.datetime.now() - CACHED_SOURCE[1]).days < CACHED_SOURCE_TIMEOUT :
		cpi = CACHED_SOURCE[0]
	else:
		cpi           = CPI()
		CACHED_SOURCE = (cpi, datetime.datetime.now())

	inflation     = Inflation(source=cpi)

	def closest_ajustment_reference_date():
	    cpi_closest = cpi.closest(
	        country = country,
	        date    = datetime.date.today(),
	        limit   = datetime.timedelta(366*5))
	    return cpi_closest.date
	_year = year
	for i in range(INFLATION_REFERENCE_RETRY):
		reference_date = closest_ajustment_reference_date()
		try:
			return (inflation.inflate(amount, reference_date, datetime.date(_year, 1, 1), country),
				reference_date.year )
		except KeyError:
			_year = _year - 1
	raise Exception("no date found for inflation. Asked for %s and tested up to %s (%s)" % (year, _year + 1, country))

if __name__ == "__main__":
	print get_inflation(200, 2009, 'fra')
	print get_inflation(200, 2009, 'fra')

# EOF
