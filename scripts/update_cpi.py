#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 23-Oct-2013
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
Update the CPI local data from a remote source,
Update the available years list
"""

import os
from django.conf import settings
from subprocess import call

os.environ['PYTHONPATH'] = ROOT_PATH = settings.ROOT_PATH

if __name__ == "__main__":
    cpi2datapackage_script  = os.path.join(ROOT_PATH, 'scripts', 'cpi2datapackage.py')
    updateavailyears_script = os.path.join(ROOT_PATH, 'scripts', 'update_available_years.py')
    cpi_output              = os.path.join(ROOT_PATH, "data", "cpi", "cpi.csv")
    print "Updating %s from remote source" % cpi_output
    call([cpi2datapackage_script, "-o", cpi_output])
    print "Updating available years list"
    call([updateavailyears_script])
    exit()

# EOF
