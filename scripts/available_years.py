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
# Last mod : 07-Aug-2013
# -----------------------------------------------------------------------------
"""

Create a json file which contains the list of available years for each country
in the `data/cpi/cpi.csv` file.

This json file will be used in order to check the user entries for dates and
to show dynamically the available dates if the country is known.

"""
import csv
import json
results = {}

with open("data/cpi/cpi.csv") as cpi_file:
    spamreader = csv.reader(cpi_file, delimiter=',', quotechar='"')
    spamreader.next()
    for row in spamreader:
        country, code, year, cpi = row
    	if not code in results:
    		results[code] = []
    	results[code].append(int(year))

with open("data/years_available_per_country.json", "w") as output:
	output.write(json.dumps(results))

# EOF
