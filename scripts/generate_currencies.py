#!/usr/bin/env python
# coding=utf-8
import os, requests, sys
from django.conf import settings

os.environ['PYTHONPATH'] = ROOT_PATH = settings.ROOT_PATH

CURRENCIES = {
    "USD": {
        "name": "US dollar", 
        "symbol": "$",
        "priority": 1
    },
    "EUR": {
        "name": "EU euro", 
        "symbol": "€",
        "priority": 1
    },
    "JPY": {
        "name": "Japanese yen", 
        "symbol": "¥",
        "priority": 1
    },
    "GBP": {
        "name": "British pound", 
        "symbol": "£",
        "priority": 1
    },
    "AUD": {
        "name": "Australian dollar", 
        "symbol": "$",
        "priority": 2
    },
    "CHF": {
        "name": "Swiss franc", 
        "symbol": "CHF",
        "priority": 2
    },
    "CAD": {
        "name": "Canadian dollar", 
        "symbol": "$",
        "priority": 2
    },
    "HKD": {
        "name": "Hong Kong SAR dollar", 
        "symbol": "$",
        "priority": 2
    },
    "SEK": {
        "name": "Swedish krona", 
        "symbol": "kr",
        "priority": 2
    },
    "NZD": {
        "name": "New Zealand dollar", 
        "symbol": "$",
        "priority": 2
    },
    "KRW": {
        "name": "South Korean won", 
        "symbol": "₩",
        "priority": 2
    },
    "SGD": {
        "name": "Singapore dollar", 
        "symbol": "$",
        "priority": 2
    },
    "NOK": {
        "name": "Norwegian krone", 
        "symbol": "kr",
        "priority": 2
    },
    "MXN": {
        "name": "Mexican peso", 
        "symbol": "$",
        "priority": 2
    },
    "INR": {
        "name": "Indian rupee", 
        "symbol": "₹",
        "priority": 2
    },
    "CNY": {
        "name": "Chinese yuan renminbi", 
        "symbol": "¥",
        "priority": 3
    },
    "BRL": {
        "name": "Brazilian real", 
        "symbol": "R$",
        "priority": 3
    },
    "TWD": {
        "name": "Taiwan New dollar", 
        "symbol": "NT$",
        "priority": 3
    },
    "RUB": {
        "name": "Russian ruble", 
        "symbol": "руб",
        "priority": 3
    },
    "THB": {
        "name": "Thai baht", 
        "symbol": "฿",
        "priority": 3
    },
    "MYR": {
        "name": "Malaysian ringgit", 
        "symbol": "RM",
        "priority": 3
    },
    "TRY": {
        "name": "Turkish lira", 
        "symbol": "\u20BA",
        "priority": 3
    },
    "SAR": {
        "name": "Saudi riyal", 
        "symbol": "﷼",
        "priority": 3
    },
    "IDR": {
        "name": "Indonesian rupiah", 
        "symbol": "Rp",
        "priority": 3
    },
    "PLN": {
        "name": "Polish zloty", 
        "symbol": "zł",
        "priority": 3
    },
    "ZAR": {
        "name": "South African rand", 
        "symbol": "R",
        "priority": 3
    },
    "AED": {
        "name": "UAE dirham", 
        "symbol": "",
        "priority": 3
    },
    "DKK": {
        "name": "Danish krone", 
        "symbol": "kr",
        "priority": 3
    },
    "ILS": {
        "name": "Israeli new shekel", 
        "symbol": "₪",
        "priority": 3
    },
    "CLP": {
        "name": "Chilean peso", 
        "symbol": "$",
        "priority": 3
    },
    "EGP": {
        "name": "Egyptian pound", 
        "symbol": "£",
        "priority": 3
    },
    "VEF": {
        "name": "Venezuelan bolivar fuerte", 
        "symbol": "Bs",
        "priority": 3
    },
    "VND": {
        "name": "Vietnamese dong", 
        "symbol": "₫",
        "priority": 3
    },
    "CZK": {
        "name": "Czech koruna", 
        "symbol": "Kč",
        "priority": 3
    },
    "COP": {
        "name": "Colombian peso", 
        "symbol": "$",
        "priority": 3
    },
    "DZD": {
        "name": "Algerian dinar", 
        "symbol": "دج",
        "priority": 3
    },
    "ARS": {
        "name": "Argentine peso", 
        "symbol": "$",
        "priority": 3
    }
}

# OpenExchangeRates API base url
OER_API_BASE_URL = "http://openexchangerates.org/api/latest.json?app_id=%s"

def get_rates(app_id):
    r = requests.get(OER_API_BASE_URL % app_id)
    return r.json()


def create_currency_object(iso_code, rate):
    # find and create the appropriated currency object 
    currency = CURRENCIES[iso_code]
    model_name = 'currency.currency'
    currency = {
        'pk': iso_code,
        'model': model_name,
        'fields': {
            'iso_code': iso_code,
            'rate': rate,
            'name': currency['name'],
            'symbol': currency['symbol'],
            'priority': currency['priority']
        }
    }
    return currency

def create_currencies(api_key):
    # get the latest exchange rates 
    latest_rates = get_rates(api_key)['rates']
    currencies = []

    for iso_code in latest_rates:
        if iso_code in CURRENCIES:
            rate     = latest_rates[iso_code]
            currency = create_currency_object(iso_code=iso_code, rate=rate)
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
        fixtures_path = ROOT_PATH + '/webapp/currency/fixtures/initial_data.json'
        with open(fixtures_path, 'w') as outfile:
            import json
            json.dump(currencies, outfile)

else:
    print "\nMissing arguments, please check usage:\n\n"
    show_usage()
