#!/usr/bin/env python
import os, requests, sys
from django.conf import settings
from django.core.management import setup_environ

os.environ['PYTHONPATH'] = ROOT_PATH = settings.ROOT_PATH
from spendingstories.core.models import Currency


# OpenExchangeRates API base url
OER_API_BASE_URL = "http://openexchangerates.org/api/latest.json?app_id=%s"

def get_rates(app_id):
    r = requests.get(OER_API_BASE_URL % app_id)
    return r.json()


def create_currency_object(iso_code, rate, pk):
    model_name = 'core.currency'
    currency = {
        'pk': pk,
        'model': model_name,
        'fields': {
            'iso_code': iso_code,
            'rate': rate
        }
    }
    return currency

def create_currencies(api_key):
    json = get_rates(api_key)
    latest_rates = json['rates']
    currencies = []
    currency_id = 1

    for iso_code in latest_rates:
        rate         = latest_rates[iso_code]
        currency     = create_currency_object(
            iso_code=iso_code, 
            rate=rate, 
            pk=currency_id
        )
        print currency 
        currency_id += 1
        currencies.append(currency)

    return currencies

def show_usage():
    print "Currencies rates generator usage.\n\n"\
        "\t./generate_currencies.py <OpenExchangeRates API key>\n"\
        "\t\tWill generate the currencies rates for this app\n"\
        "\t./generate_currencies.py -h|--help\n"\
        "\t\tShow this help"

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == None or arg == "-h" or arg == '--help':
        show_usage()
    else:
        currencies = create_currencies(arg)
        fixtures_path = ROOT_PATH + '/spendingstories/core/fixtures/currencies.json'
        with open(fixtures_path, 'w') as outfile:
            import json
            json.dump(currencies, outfile)
        
else:
    print "\nMissing arguments, please check usage:\n\n"
    show_usage() 





