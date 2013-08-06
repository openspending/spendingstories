#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 06-Aug-2013
# Last mod : 06-Aug-2013
# -----------------------------------------------------------------------------
from economics import Inflation, CPI
import datetime

# -----------------------------------------------------------------------------
#
#    INFLATION
#
# -----------------------------------------------------------------------------
CPI       = CPI()
INFLATION = Inflation(CPI)

def get_inflation(amount, year, country):
	def closest_ajustment_year():
	    cpi_closest = CPI.closest(
	        country = country,
	        date    = datetime.date.today(),
	        limit   = datetime.timedelta(366*3))
	    return cpi_closest.date
	try:
		return (INFLATION.inflate(amount, closest_ajustment_year(), datetime.date(year, 1, 1), country),
			closest_ajustment_year().year )
	except KeyError:
		return get_inflation(amount, year - 1, country)

# EOF
