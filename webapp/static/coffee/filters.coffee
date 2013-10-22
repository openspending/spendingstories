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
                _fromCurrency = Currency.list[fromCurrency]
                _toCurrency = Currency.list[toCurrency]
                converted = parseInt(value)
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
                return Humanize.humanizeValue converted, _toCurrency.name, (converted > 1)
            
        ]
    )
    .filter("humanizeValue", ["Currency","humanizeService", (Currency, Humanize)->
            return (value, currency="USD") ->
                return null unless angular.isNumber value
                _currency = Currency.list[currency]
                if _currency? then Humanize.humanizeValue value, _currency.name

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
 
                if result < Math.pow(10,3) || result > Math.pow(10, 15)
                    result = Humanize.intcomma(result, decimals)
                else
                    result = Humanize.intword(result, decimals)
 
                if use_percentage
                    result += '%'
                    wording_end = $translate('HUMANIZE_OF')
                 else
                    wording_end = Humanize.pluralize
                                        value: value
                                        single: $translate('HUMANIZE_MULTIPLE')
                                        plural: $translate('HUMANIZE_MULTIPLE_PLURAL')

                return "#{wording_begin} #{result} #{wording_end}"

        ]
    )
    .filter("cardEquivalent", ["searchService", "Currency","humanizeService", (searchService, Currency, Humanize)->
            return (story)->
                return null unless story?
                Humanize.humanizeEquivalence story,
                    currency: Currency.list[searchService.currency]
                    value:searchService.query_usd
        ]
    )