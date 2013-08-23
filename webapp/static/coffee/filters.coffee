OSS = OpenSpendingStories = window.SpendingStories = window.SpendingStories || 
    humanize: (value, suffix, plural=false)->
        if plural
            suffix += 's'
        if value < Math.pow(10, 6) || value > Math.pow(10, 15)
            Humanize.intcomma(value) + " " + suffix
        else
            Humanize.intword(value) + " " + suffix

    round: (value, decimals_number=2) ->
        return null unless angular.isNumber value
        return Humanize.intcomma(value, decimals_number)

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
                OSS.humanize(converted, toCurrency.name, (converted > 1))
        ]
    )
    .filter("humanizeCurrency", ["Currency", (Currency)->
            return (value, currency="USD")->
                return null unless angular.isNumber value
                toCurrency = Currency.list[currency]
                suffix = if toCurrency? then toCurrency.name else currency
                OSS.humanize(value, suffix, ((value > 1) && toCurrency?)) 
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
    .filter("queryPercentage", ["Search", (Search) -> 
            return (value_usd)->

                percentage = (Search.query_usd / value_usd) * 100
                wording_begin = "are"
                use_percentage = true
                if percentage > 1
                    wording_begin += " nearly"
                    if percentage > 100
                        percentage = OSS.round (percentage / 100), 1
                        use_percentage = false
                    else
                        percentage = OSS.round(percentage, 0)
                else
                    if percentage < 0.01
                        wording_begin += " less than"
                        percentage = 0.01
                    else
                        wording_begin += " almost"
                        percentage = OSS.round(percentage, 2)
                if use_percentage
                    wording_end = "#{percentage}% of"
                else
                    wording_end = "#{percentage} times"

                return "#{wording_begin} #{wording_end}"
        ]
    )