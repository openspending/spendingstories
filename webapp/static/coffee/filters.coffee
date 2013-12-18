angular
    .module('storiesFilters', [])
    .filter('thousandSeparator', ['humanizeService', (Humanize)-> Humanize.intcomma ])
    .filter('truncate', -> 
        # took from https://gist.github.com/danielcsgomes/2478654
        return (text, length, end='') ->
            if !angular.isString(text)
                return text
            if isNaN(length)
                length = 10

            if text.length <= length || (text.length - end.length) <= length
                return text
            else
                return String(text).substring(0, length-end.length) + end
    )
    .filter("toQueryCurrency", ["searchService", "Currency","humanizeService", (searchService, Currency, Humanize)->  
            return (value, fromCurrency='USD', toCurrency=searchService.currency, decimals=2)-> 
                _fromCurrency = Currency.get(fromCurrency)
                _toCurrency = Currency.get(toCurrency)
                if value > 1
                    converted = parseInt(value)
                else
                    converted = value
                return null unless angular.isNumber(converted) and _fromCurrency? and _toCurrency? 
                # Convertion needed
                if _toCurrency.iso_code isnt _fromCurrency.iso_code
                    # Initial value must be converted to dollars
                    if _fromCurrency.iso_code isnt 'USD'
                        # Initial value is now converted to dollar
                        converted = converted/_fromCurrency.rate
                    # If the final currency isn't dollar
                    if _toCurrency.iso_code isnt 'USD'
                        # The value is now into the targeted currency
                        converted = converted*_toCurrency.rate
                pow = Math.pow 10, decimals
                converted = (Math.round converted * pow) / pow
                return Humanize.localizedValue converted, _toCurrency
            
        ]
    )
    .filter("humanizeValue", ["Currency","humanizeService", (Currency, Humanize)->
            return (value, currency="USD") ->
                return null unless angular.isNumber value
                _currency = Currency.get(currency)
                if _currency? then Humanize.localizedValue value, _currency

        ]
    )    
    .filter("humanizeValueISO", ["Currency","humanizeService", (Currency, Humanize)->
            return (value, currency="USD") ->
                return null unless angular.isNumber value
                _currency = Currency.get(currency)
                if _currency? then Humanize.humanizeValue value, _currency.iso_code, false

        ]
    )
    .filter("nl2br", ->
        return (str='')-> (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1<br />$2')
    )
    .filter("linkDomain", ->
        return (href)->
            if angular.isString(href)
                return href.split('/').slice(2)[0]
            else 
                return href
    )
    .filter("thousandRound", ->
        return (n)-> Math.round(n/1000)*1000
    )
    .filter("simpleMillion", ->
        return (n)-> Math.round(n/Math.pow(10, 5))/10
    )
    .filter("decimalSeparator", ->
        return (n, dec=".")-> (n+"").replace /\./, dec
    )
    .filter("queryEquivalent", ['$translate', "searchService","humanizeService", ($translate, searchService, Humanize)-> 
            return (d)->
                return "" unless d.current_value_usd?
                value = d.current_value_usd
                ratio = searchService.query_usd / value 
                percentage = ratio * 100
                use_percentage = true
                decimals = 1

                wording_begin = Humanize.pluralize(value: searchService.query, single: $translate('HUMANIZE_IS'), plural: $translate('HUMANIZE_ARE'))
                if percentage > 100
                    use_percentage = false
                    result = ratio
                else
                    result = percentage
                    if percentage >= 1 
                        decimals = 0
                    if percentage < 1
                        decimals = Humanize.getDecimalNumber(percentage)
                        if decimals == 0
                            decimals = 1

                result = Humanize.round result, decimals
                # if result number have less decimals than the original float 
                # we need to be sure to have the right number of decimals  
                decimals = Humanize.getDecimalNumber result 
 
                if result < Math.pow(10,3) || result > Math.pow(10, 15)
                    result_str = Humanize.intcomma(result, decimals)
                else
                    result_str = Humanize.intword(result, decimals)
 
                if use_percentage
                    result_str += '%'
                    wording_end = $translate('HUMANIZE_OF')
                    if result <= Math.pow(10, -5) and percentage < result 
                        lt = $translate('HUMANIZE_LESS_THAN')
                        wording_begin = "#{wording_begin} #{lt}"
                 else
                    wording_end = Humanize.pluralize
                                        value: value
                                        single: $translate('HUMANIZE_MULTIPLE')
                                        plural: $translate('HUMANIZE_MULTIPLE_PLURAL')

                return "#{wording_begin} #{result_str} #{wording_end}"

        ]
    )
    .filter("cardEquivalent", ["searchService", "Currency","humanizeService", (searchService, Currency, Humanize)->
            return (story)->
                return null unless story?
                Humanize.humanizeEquivalence story,
                    currency: Currency.get(searchService.currency)
                    value:searchService.query_usd
        ]
    )
    .filter("localizedCountryName", ['$translate', ($translate)->
            return (country)->
                return null unless country? # short fail 
                c_name = country.value or country.name
                c_iso_code = country.key or country.iso_code or null
                i18n_key = "COUNTRY_#{c_iso_code}" if c_iso_code?
                localized = $translate(i18n_key)
                if localized is i18n_key
                    localized = c_name
                localized
        ]
    )
    .filter("localizedCurrencyName", ['$translate', ($translate)->
            return (currency)->
                return null unless currency? # short fail 
                c_name = currency.value or currency.name
                c_iso_code = currency.key or currency.iso_code or null
                i18n_key = "CURRENCY_#{c_iso_code}" if c_iso_code?
                localized = $translate(i18n_key)
                if localized is i18n_key
                    localized = c_name
                localized[0].toUpperCase() + localized.substring(1)
        ]
    )
    .filter("localizedLanguageName", ['$translate', ($translate)->
            return (lang)->
                return null unless lang? # short fail
                l_name = lang.value or lang.name
                l_code = lang.key or lang.code or null
                i18n_key = "LANGUAGE_#{l_code.toUpperCase()}" if l_code?
                localized = $translate(i18n_key)
                if localized is i18n_key
                    localized = l_name
                localized[0].toUpperCase() + localized.substring(1)
        ]
    )
