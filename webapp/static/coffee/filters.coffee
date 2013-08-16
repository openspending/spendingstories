thousandSeparator = (nStr, sep=",")->
    nStr = "" + (nStr or "")
    x = nStr.split(".")
    x1 = x[0]
    x2 = (if x.length > 1 then "." + x[1] else "")
    rgx = /(\d+)(\d{3})/
    x1 = x1.replace(rgx, "$1" + sep + "$2") while rgx.test(x1)
    x1 + x2

angular
    .module('storiesFilters', [])
    .filter("thousandSeparator", ->thousandSeparator)
    .filter("toQueryCurrency", ["Search", "Currency", (Search, Currency)->  
            return (value, fromCurrency='USD', toCurrency=Search.currency, decimals=2)->                 
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

                    thousandSeparator(
                        # Round the value 
                        Math.round(
                            converted * Math.pow(10, decimals)
                        ) / Math.pow(10, decimals) 
                    # Add the currency code as prefix
                    ) + " " + toCurrency.name
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