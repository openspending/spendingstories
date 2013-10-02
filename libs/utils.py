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
