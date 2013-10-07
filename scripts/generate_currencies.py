#!/usr/bin/env python
import os, requests, sys
from django.conf import settings

os.environ['PYTHONPATH'] = ROOT_PATH = settings.ROOT_PATH

currencies = {
    "CNY": { "name" : "Chinese yuan renminbi", "symbol" : "&#165;" },
    "JPY": { "name" : "Japanese yen", "symbol" : "&#165;" },
    "USD": { "name" : "US dollar", "symbol" : "&#36;" },
    "EUR": { "name" : "EU euro", "symbol" : "&#8364;" },
    "GBP": { "name" : "British pound", "symbol" : "&#163;" },
    "BRL": { "name" : "Brazilian real", "symbol" : "&#82;&#36;" },
    "AUD": { "name" : "Australian dollar", "symbol" : "&#36;" },
    "KRW": { "name" : "South Korean won", "symbol" : "&#8361;" },
    "CAD": { "name" : "Canadian dollar", "symbol" : "&#36;" },
    "INR": { "name" : "Indian rupee", "symbol" : "" },
    "CHF": { "name" : "Swiss franc", "symbol" : "&#67;&#72;&#70;" },
    "HKD": { "name" : "Hong Kong SAR dollar", "symbol" : "&#36;" },
    "TWD": { "name" : "Taiwan New dollar", "symbol" : "&#78;&#84;&#36;" },
    "RUB": { "name" : "Russian ruble", "symbol" : "&#1088;&#1091;&#1073;" },
    "MXN": { "name" : "Mexican peso", "symbol" : "&#36;" },
    "THB": { "name" : "Thai baht", "symbol" : "&#3647;" },
    "MYR": { "name" : "Malaysian ringgit", "symbol" : "&#82;&#77;" },
    "SEK": { "name" : "Swedish krona", "symbol" : "&#107;&#114;" },
    "SGD": { "name" : "Singapore dollar", "symbol" : "&#36;" },
    "TRY": { "name" : "Turkish lira", "symbol" : "" },
    "SAR": { "name" : "Saudi riyal", "symbol" : "&#65020;" },
    "IDR": { "name" : "Indonesian rupiah", "symbol" : "&#82;&#112;" },
    "NOK": { "name" : "Norwegian krone", "symbol" : "&#107;&#114;" },
    "PLN": { "name" : "Polish zloty", "symbol" : "&#122;&#322;" },
    "ZAR": { "name" : "South African rand", "symbol" : "&#82;" },
    "AED": { "name" : "UAE dirham", "symbol" : "" },
    "DKK": { "name" : "Danish krone", "symbol" : "&#107;&#114;" },
    "ILS": { "name" : "Israeli new shekel", "symbol" : "&#8362;" },
    "CLP": { "name" : "Chilean peso", "symbol" : "&#36;" },
    "EGP": { "name" : "Egyptian pound", "symbol" : "&#163;" },
    "VEF": { "name" : "Venezuelan bolivar fuerte", "symbol" : "&#66;&#115;" },
    "VND": { "name" : "Vietnamese dong", "symbol" : "&#8363;" },
    "NZD": { "name" : "New Zealand dollar", "symbol" : "&#36;" },
    "CZK": { "name" : "Czech koruna", "symbol" : "&#75;&#269;" },
    "COP": { "name" : "Colombian peso", "symbol" : "&#36;" },
    "DZD": { "name" : "Algerian dinar", "symbol" : "" },
    "ARS": { "name" : "Argentine peso", "symbol" : "&#36;" }
}


# OpenExchangeRates API base url
OER_API_BASE_URL = "http://openexchangerates.org/api/latest.json?app_id=%s"

def get_rates(app_id):
    r = requests.get(OER_API_BASE_URL % app_id)
    return r.json()


def create_currency_object(name, iso_code, rate, symbol):
    model_name = 'currency.currency'
    currency = {
        'pk': iso_code,
        'model': model_name,
        'fields': {
            'iso_code': iso_code,
            'rate': rate,
            'name': name,
            'symbol': symbol
        }
    }
    return currency

def create_currencies(api_key):
    json = get_rates(api_key)
    latest_rates = json['rates']
    currs = []

    for iso_code in latest_rates:
        if iso_code in currencies:
            currency     = currencies[iso_code]
            name         = currency["name"]
            rate         = latest_rates[iso_code]
            symbol       = currency["symbol"]
            currency     = create_currency_object(
                name=name,
                iso_code=iso_code,
                rate=rate,
                symbol=symbol
            )
            currs.append(currency)

    return currs

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





