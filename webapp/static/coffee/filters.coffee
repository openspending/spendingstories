humanize = (value, suffix, plural=false)->
    if plural
        suffix += 's'
    if value < Math.pow(10, 6) || value > Math.pow(10, 15)
        Humanize.intcomma(value) + " " + suffix
    else
        Humanize.intword(value) + " " + suffix

angular
    .module('storiesFilters', [])
    .filter("thousandSeparator", -> Humanize.intcomma)
    .filter("toQueryCurrency", ["Search", "Currency", (Search, Currency)->  
            return (value, fromCurrency='USD', toCurrency=Search.currency, decimals=2)->    
                return null unless angular.isNumber value
                fromCurrency = Currency.list[fromCurrency]      
                toCurrency   = Currency.list[toCurrency]
                converted = value
                
                if fromCurrency? and toCurrency?                             
                    # Convertion needed
                    if toCurrency.iso_code isnt fromCurrency.iso_code
                        # Initial value must be converted to dollars
                        if fromCurrency isnt 'USD'
                            # Initial value is now converted to dollar
                            converted = converted/fromCurrency.rate
                        # If the final currency isn't dollar
                        if toCurrency isnt 'USD'
                            # The value is now into the targeted currency
                            converted = converted*toCurrency.rate
                humanize(converted, toCurrency.name, (converted > 1))
        ]
    )
    .filter("humanizeCurrency", ["Currency", (Currency)->
            return (value, currency="USD")->
                return null unless angular.isNumber value
                toCurrency = Currency.list[currency]
                suffix = if toCurrency? then toCurrency.name else currency
                humanize(value, suffix, ((value > 1) && toCurrency?)) 
        ]
    )
    .filter("nl2br", ->
        return (str='')-> (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1<br />$2')
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