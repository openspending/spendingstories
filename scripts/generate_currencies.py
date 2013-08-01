#!/usr/bin/env python
import os, requests, sys
from django.conf import settings
from django.core.management import setup_environ

os.environ['PYTHONPATH'] = ROOT_PATH = settings.ROOT_PATH
from spendingstories.core.models import Currency

names = {
    "AFN":"Afghanistan afghani",
    "ALL":"Albanian lek",
    "DZD":"Algerian dinar",
    "AOA":"Angolan kwanza",
    "ARS":"Argentine peso",
    "AMD":"Armenian dram",
    "AWG":"Aruban guilder",
    "AUD":"Australian dollar",
    "AZN":"Azerbaijanian new manat",
    "BSD":"Bahamian dollar",
    "BHD":"Bahraini dinar",
    "BDT":"Bangladeshi taka",
    "BBD":"Barbados dollar",
    "BYR":"Belarusian ruble",
    "BZD":"Belize dollar",
    "BMD":"Bermudian dollar",
    "BTN":"Bhutan ngultrum",
    "BOB":"Bolivian boliviano",
    "BWP":"Botswana pula",
    "BRL":"Brazilian real",
    "GBP":"British pound",
    "BND":"Brunei dollar",
    "BGN":"Bulgarian lev",
    "BIF":"Burundi franc",
    "KHR":"Cambodian riel",
    "CAD":"Canadian dollar",
    "CVE":"Cape Verde escudo",
    "KYD":"Cayman Islands dollar",
    "XOF":"CFA franc BCEAO",
    "XAF":"CFA franc BEAC",
    "XPF":"CFP franc",
    "CLP":"Chilean peso",
    "CNY":"Chinese yuan renminbi",
    "COP":"Colombian peso",
    "KMF":"Comoros franc",
    "CDF":"Congolese franc",
    "CRC":"Costa Rican colon",
    "HRK":"Croatian kuna",
    "CUP":"Cuban peso",
    "CZK":"Czech koruna",
    "DKK":"Danish krone",
    "DJF":"Djibouti franc",
    "DOP":"Dominican peso",
    "XCD":"East Caribbean dollar",
    "EGP":"Egyptian pound",
    "SVC":"El Salvador colon",
    "ERN":"Eritrean nakfa",
    "EEK":"Estonian kroon",
    "ETB":"Ethiopian birr",
    "EUR":"EU euro",
    "FKP":"Falkland Islands pound",
    "FJD":"Fiji dollar",
    "GMD":"Gambian dalasi",
    "GEL":"Georgian lari",
    "GHS":"Ghanaian new cedi",
    "GIP":"Gibraltar pound",
    "XAU":"Gold (ounce)",
    "XFO":"Gold franc",
    "GTQ":"Guatemalan quetzal",
    "GNF":"Guinean franc",
    "GYD":"Guyana dollar",
    "HTG":"Haitian gourde",
    "HNL":"Honduran lempira",
    "HKD":"Hong Kong SAR dollar",
    "HUF":"Hungarian forint",
    "ISK":"Icelandic krona",
    "XDR":"IMF special drawing right",
    "INR":"Indian rupee",
    "IDR":"Indonesian rupiah",
    "IRR":"Iranian rial",
    "IQD":"Iraqi dinar",
    "ILS":"Israeli new shekel",
    "JMD":"Jamaican dollar",
    "JPY":"Japanese yen",
    "JOD":"Jordanian dinar",
    "KZT":"Kazakh tenge",
    "KES":"Kenyan shilling",
    "KWD":"Kuwaiti dinar",
    "KGS":"Kyrgyz som",
    "LAK":"Lao kip",
    "LVL":"Latvian lats",
    "LBP":"Lebanese pound",
    "LSL":"Lesotho loti",
    "LRD":"Liberian dollar",
    "LYD":"Libyan dinar",
    "LTL":"Lithuanian litas",
    "MOP":"Macao SAR pataca",
    "MKD":"Macedonian denar",
    "MGA":"Malagasy ariary",
    "MWK":"Malawi kwacha",
    "MYR":"Malaysian ringgit",
    "MVR":"Maldivian rufiyaa",
    "MRO":"Mauritanian ouguiya",
    "MUR":"Mauritius rupee",
    "MXN":"Mexican peso",
    "MDL":"Moldovan leu",
    "MNT":"Mongolian tugrik",
    "MAD":"Moroccan dirham",
    "MZN":"Mozambique new metical",
    "MMK":"Myanmar kyat",
    "NAD":"Namibian dollar",
    "NPR":"Nepalese rupee",
    "ANG":"Netherlands Antillian guilder",
    "NZD":"New Zealand dollar",
    "NIO":"Nicaraguan cordoba oro",
    "NGN":"Nigerian naira",
    "KPW":"North Korean won",
    "NOK":"Norwegian krone",
    "OMR":"Omani rial",
    "PKR":"Pakistani rupee",
    "XPD":"Palladium (ounce)",
    "PAB":"Panamanian balboa",
    "PGK":"Papua New Guinea kina",
    "PYG":"Paraguayan guarani",
    "PEN":"Peruvian nuevo sol",
    "PHP":"Philippine peso",
    "XPT":"Platinum (ounce)",
    "PLN":"Polish zloty",
    "QAR":"Qatari rial",
    "RON":"Romanian new leu",
    "RUB":"Russian ruble",
    "RWF":"Rwandan franc",
    "SHP":"Saint Helena pound",
    "WST":"Samoan tala",
    "STD":"Sao Tome and Principe dobra",
    "SAR":"Saudi riyal",
    "RSD":"Serbian dinar",
    "SCR":"Seychelles rupee",
    "SLL":"Sierra Leone leone",
    "XAG":"Silver (ounce)",
    "SGD":"Singapore dollar",
    "SBD":"Solomon Islands dollar",
    "SOS":"Somali shilling",
    "ZAR":"South African rand",
    "KRW":"South Korean won",
    "LKR":"Sri Lanka rupee",
    "SDG":"Sudanese pound",
    "SRD":"Suriname dollar",
    "SZL":"Swaziland lilangeni",
    "SEK":"Swedish krona",
    "CHF":"Swiss franc",
    "SYP":"Syrian pound",
    "TWD":"Taiwan New dollar",
    "TJS":"Tajik somoni",
    "TZS":"Tanzanian shilling",
    "THB":"Thai baht",
    "TOP":"Tongan pa'anga",
    "TTD":"Trinidad and Tobago dollar",
    "TND":"Tunisian dinar",
    "TRY":"Turkish lira",
    "TMT":"Turkmen new manat",
    "AED":"UAE dirham",
    "UGX":"Uganda new shilling",
    "XFU":"UIC franc",
    "UAH":"Ukrainian hryvnia",
    "UYU":"Uruguayan peso uruguayo",
    "USD":"US dollar",
    "UZS":"Uzbekistani sum",
    "VUV":"Vanuatu vatu",
    "VEF":"Venezuelan bolivar fuerte",
    "VND":"Vietnamese dong",
    "YER":"Yemeni rial",
    "ZMK":"Zambian kwacha",
    "ZWL":"Zimbabwe dollar"
}


# OpenExchangeRates API base url
OER_API_BASE_URL = "http://openexchangerates.org/api/latest.json?app_id=%s"

def get_rates(app_id):
    r = requests.get(OER_API_BASE_URL % app_id)
    return r.json()


def create_currency_object(name, iso_code, rate):
    model_name = 'core.currency'
    currency = {
        'pk': iso_code,
        'model': model_name,
        'fields': {
            'iso_code': iso_code,
            'rate': rate,
            'name': name
        }
    }
    return currency

def create_currencies(api_key):
    json = get_rates(api_key)
    latest_rates = json['rates']
    currencies = []
    currency_id = 1

    for iso_code in latest_rates:
        if iso_code in names:
            name         = names[iso_code]
            rate         = latest_rates[iso_code]
            currency     = create_currency_object(
                name=name, 
                iso_code=iso_code, 
                rate=rate
            )
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





