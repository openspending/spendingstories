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
# Last mod : 23-Oct-2013
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

"""

Create or update a json file which contains the list of available years for each country
in the `data/cpi/cpi.csv` file.

This json file will be used in order to check the user entries for dates and
to show dynamically the available dates if the country is known.

"""

import csv
import json
import os
from django.conf import settings

ROOT_PATH = settings.ROOT_PATH

if __name__ == "__main__":

    results = {}

    with open(os.path.join(ROOT_PATH, "data", "cpi", "cpi.csv")) as cpi_file:
        spamreader = csv.reader(cpi_file, delimiter=',', quotechar='"')
        spamreader.next()
        for row in spamreader:
            country, code, year, cpi = row
            if not code in results:
                results[code] = []
            results[code].append(int(year))

    with open(os.path.join(ROOT_PATH, "data", "years_available_per_country.json"), "w") as output:
        output.write(json.dumps(results))

    exit()

# EOF
