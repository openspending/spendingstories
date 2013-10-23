#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Pierre Bellon                                    <pbellon@gmail.com>
#          Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 31-Aug-2013
# Last mod : 23-Oct-2013
# -----------------------------------------------------------------------------
import os, requests, sys
from django.conf import settings
from webapp.currency.models import Currency
from django.core import management

os.environ['PYTHONPATH'] = ROOT_PATH = settings.ROOT_PATH

# OpenExchangeRates API base url
OER_API_BASE_URL = "http://openexchangerates.org/api/latest.json?app_id=%s"
FIXTURES_PATH    = ROOT_PATH + '/webapp/currency/fixtures/initial_data.json'

def get_rates(app_id):
    r = requests.get(OER_API_BASE_URL % app_id)
    return r.json()['rates']

def show_usage():
    print "Currencies rates generator usage.\n\n"\
        "\t./generate_currencies.py <OpenExchangeRates API key>\n"\
        "\t\tWill generate the currencies rates for this app\n"\
        "\t./generate_currencies.py -h|--help\n"\
        "\t\tShow this help"

if __name__ == "__main__":

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == None or arg == "-h" or arg == '--help':
            show_usage()
        else:
            rates = get_rates(arg)
            for currency in Currency.objects.all():
                currency.rate = rates[currency.iso_code]
                currency.save()
            # save in fixtures
            with open(FIXTURES_PATH, 'w') as f:
                management.call_command('dumpdata', 'currency', stdout=f)
    else:
        print "\nMissing arguments, please check usage:\n\n"
        show_usage()

    exit()

# EOF
