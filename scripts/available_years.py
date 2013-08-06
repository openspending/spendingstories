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

import csv
import json
from pprint import pprint as pp
results = {}

with open("data/cpi/cpi.csv") as cpi_file:
    spamreader = csv.reader(cpi_file, delimiter=',', quotechar='"')

    for row in spamreader:
        country, code, year, cpi = row
    	if not code in results:
    		results[code] = []
    	results[code].append(year)
print json.dumps(results)
    # 	print row

with open("data/years_available_per_country.json", "w") as output:
	output.write(json.dumps(results))
