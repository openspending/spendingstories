humanize = (value)->
    humanized = Humanize.intword(value) 
    if value < Math.pow(10, 6) || value > Math.pow(10, 15)
        humanized = Humanize.intcomma(value)
    return humanized

angular
    .module('storiesFilters', [])
    .filter("humanize", -> humanize)
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

                humanize(converted) + " " + toCurrency.name
        ]
    )
    .filter("humanizeCurrency", ["Currency", (Currency)->
            return (value, currency="USD")->
                return null unless angular.isNumber value
                toCurrency = Currency.list[currency]            
                suffix = if toCurrency? then toCurrency.name else currency

                if value < Math.pow(10, 6) || value > Math.pow(10, 15)
                    Humanize.intcomma(value) + " " + suffix
                else
                    Humanize.intword(value) + " " + suffix
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