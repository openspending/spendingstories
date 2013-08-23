OSS = OpenSpendingStories = window.SpendingStories = window.SpendingStories || 
    # TODO: avoid reduncy 
    humanize: (value, suffix, plural=false)->
        if plural
            suffix += 's'
        if value < Math.pow(10, 6) || value > Math.pow(10, 15)
            Humanize.intcomma(value) + " " + suffix
        else
            Humanize.intword(value) + " " + suffix

    getFloatPart: (value_f)->
        float_part_s = String(value_f).split('.')[1]
        return parseFloat([0,float_part_s].join('.'))

    getIntPart: (value_f)->
        return parseInt(String(value_f).split('.')[0])

    getDecimalNumber: (value_f, max_decimals=5)->
        if value_f == 0
            return 0
        float_part_s = String(value_f).split('.')[1]
        i = 0
        if value_f <= (1 / Math.pow(10, max_decimals)) 
            return max_decimals
        else
            if float_part_s
                c = float_part_s[i]
                while (c == '0') && (i <= max_decimals) 
                    do()->
                        c = float_part_s[i]
                        i += 1
        return i

    round: (value, decimals=2) ->
        if value == 0
            return 0
        result = null
        if decimals == 0
            result = @getIntPart(value)
        if decimals > 0
            if value < (1/Math.pow(10, decimals))
                return (1/Math.pow(10, decimals))
            else
                float_part = @getFloatPart(value)
                last_decimal = float_part * Math.pow(10, decimals)
                next_decimal = @getIntPart(@getFloatPart(last_decimal)*10)
                if next_decimal >= 5
                    last_decimal += 1
                else if last_decimal < 1
                    last_decimal = 1

                last_decimal_i = @getIntPart(last_decimal) 
                if next_decimal < 4 && last_decimal_i == 0
                    last_decimal_i = 1 

                float_part = @getIntPart(last_decimal) / Math.pow(10, decimals)
                result = @getIntPart(value) + float_part
        return result

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
    .filter("queryEquivalent", ["Search", (Search) -> 
            return (d)->
                value = d.current_value_usd
                ratio = Search.query_usd / value 
                percentage = ratio * 100
                use_percentage = true
                decimals = 1

                wording_begin = "are"
                if percentage > 100
                    use_percentage = false
                    result = ratio
                else
                    result = percentage
                    if percentage >= 1 
                        decimals = 0
                    if percentage < 1
                        decimals = OSS.getDecimalNumber(percentage)
                        if decimals == 0
                            decimals = 1
                result = OSS.round result, decimals


                if result < Math.pow(10,3) || result > Math.pow(10, 15)
                    result = Humanize.intcomma(result, decimals)
                else
                    result = Humanize.intword(result, decimals)

                if use_percentage
                    result = result + '%'
                    wording_end = 'of'
                else
                    wording_end = "times"

                return "are #{result} #{wording_end}"
        ]
    )