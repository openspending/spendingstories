"use strict"

OSS = OpenSpendingStories = window.SpendingStories = window.SpendingStories || 
    STORY_TYPES: 
        discrete:   'discrete'
        continous:  'over_one_year'
        population: 'per_population' # FIXME: not handled yet

    RELEVANCE_TYPES: 
        equivalent: 'equivalent'
        half:       'half'
        multiple:   'multiple'
        percentage: 'percentage'
        time:       'time'

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
        # Über rounding 
        Math.round(value * Math.pow(10, decimals))/Math.pow(10, decimals) 


    stupidPlural: (str, n)->
        result = str
        if n > 1
            result += 's'
        return result 

    randomPick: (values) ->
        values[chance.integer min: 0, max: values.length - 1 ]

    # TODO: avoid reduncy 
    humanize: (value, suffix, plural=false) ->
        if plural
            suffix += 's'
        if value < Math.pow(10, 6) || value > Math.pow(10, 15)
            Humanize.intcomma(value) + " " + suffix
        else
            Humanize.intword(value) + " " + suffix

    sentanceBuilder: (sentences, precision) ->
        s = _.find(sentences, (s)-> return precision >= s.precision[0] and precision < s.precision[1] ) or sentences[0]
        return s.value



    humanizeEquivalence: (story, query) ->
        ###
        Utility to get a human sentance for amount's equivalences
        @param story
            The story object containing every equivalence informations
            ```js
            story = {
                type: 
                relevance_type:  Equivalence type, check RELEVANCE_TYPES
                relevance_ratio: Original ratio
                relevance_value: Actual equivalence value, can be a percentage,
                                 a multiple or a time equivalence

            }
            ```
            The API calculated equivalence, can be slicly different
        @param query
            The query parameters -> {
                value: raw value entered by user
                currency: currency object got from Currencies API
            }
        ###
        switch story.relevance_type
            when @RELEVANCE_TYPES.equivalent
                return @humanizeEquivalent(story, query)
            when @RELEVANCE_TYPES.half
                return @humanizeHalf(story, query)
            when @RELEVANCE_TYPES.multiple
                return @humanizeMultiple(story, query)
            when @RELEVANCE_TYPES.percentage
                return @humanizePercentage(story, query)
            when @RELEVANCE_TYPES.time
                return @humanizeTime(story, query)

    getRatioPrecision: (a, b) ->
        ratio = Math.abs(a - b) / b
        precision = 1 - ratio
        return precision


    humanizeEquivalent: (story, query) ->
        sentences = [
                value:  "roughly matches with",
                precision: [0.90, 0.95]
            ,
                value: "almost equals"
                precision: [0.95,0.99]
            ,
                value: "is an equivalent of"
                precision: [0.99, 1]
        ]
        precision = @getRatioPrecision(story.relevance_ratio, 1)
        console.log "humanizeEquivalent, precision: ", precision
        @sentanceBuilder(sentences, precision)

    humanizeHalf: (story, query) ->
        sentences = [
                value:  "fits like half of",
                precision: [0.9, 0.99]
            ,
                value: "is half of"
                precision: [0.99,1]
        ]
        precision = @getRatioPrecision(story.relevance_ratio, 0.5)
        console.log "humanizeHalf, precision: ", precision, 
        @sentanceBuilder(sentences, precision)

    humanizeMultiple: (story, query) ->
        ratio = story.relevance_value
        return " is #{ratio} times"
    
    humanizePercentage: (story, query) ->
        ratio = story.relevance_value
        if ratio == 0
            ratio = story.relevance_ratio

        console.log ratio
        percentage = ratio * 100
        decimals = 1
        result = percentage
        if percentage >= 1 
            decimals = 0
        if percentage < 1
            decimals = OSS.getDecimalNumber(percentage)
            if decimals == 0
                decimals = 1
        result = OSS.round result, decimals
        if result < Math.pow(10,3)
            result = Humanize.intcomma(result, decimals)

        precision = @getRatioPrecision(result, story.relevance_ratio)
        sentences = [
                value:  "roughly equals #{result}% of",
                precision: [0.8, 0.95]
            ,
                value: "is #{result}% of"
                precision: [0.95,1]
        ]
        @sentanceBuilder(sentences, precision)
    
    humanizeTime: (story, value) ->
            m = story.relevance_value['months']
            w = story.relevance_value['weeks']
            d = story.relevance_value['days']
            result =  []
            months_part = @stupidPlural("#{m} month", m)
            weeks_part  = @stupidPlural("#{w} week",  w)
            days_part   = @stupidPlural("#{d} day",   d) 
            result.push(months_part) if m > 0
            result.push(weeks_part)  if w > 0 
            result.push(days_part)   if d > 0 and w == 0 or d > 1 and w > 0 
            if d is 0 and w is 0 and d is 0
                return "less than one day"
            return result.join(' ')

angular
    .module('storiesFilters', [])
    .filter('thousandSeparator', -> Humanize.intcomma)
    .filter('truncate', -> 
        # took from https://gist.github.com/danielcsgomes/2478654
        return (text, length, end) ->
            if !angular.isString(text)
                return text
            if isNaN(length)
                length = 10
 
            end = "..." unless end?

            if text.length <= length || (text.length - end.length) <= length
                return text
            else
                return String(text).substring(0, length-end.length) + end
    )
    .filter("toQueryCurrency", ["searchService", "Currency", (searchService, Currency)->  
            return (value, fromCurrency='USD', toCurrency=searchService.currency, decimals=2)->    
                return null unless angular.isNumber value
                _fromCurrency = Currency.list[fromCurrency]
                _toCurrency = Currency.list[toCurrency]
                converted = value
                
                if _fromCurrency? and _toCurrency?                             
                    # Convertion needed
                    if _toCurrency.iso_code isnt _fromCurrency.iso_code
                        # Initial value must be converted to dollars
                        if _fromCurrency.iso_code isnt 'USD'
                            # Initial value is now converted to dollar
                            converted = converted/fromCurrency.rate
                        # If the final currency isn't dollar
                        if _toCurrency.iso_code isnt 'USD'
                            # The value is now into the targeted currency
                            converted = converted*toCurrency.rate
                    OSS.humanize(converted, _toCurrency.name, (converted > 1))
                
        ]
    )
    .filter("humanizeValue", ["Currency", (Currency)->
            return (value, currency="USD") ->
                return null unless angular.isNumber value
                _currency = Currency.list[currency]
                if not _currency?
                    Currency.get(currency).then (toCurrency)->
                            OSS.humanize value, toCurrency.name or currency, value > 1 && toCurrency? 
                else
                    OSS.humanize value, _currency.name, value > 1
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
    .filter("queryEquivalent", ["searchService", (searchService) -> 
            return (d)->
                value = d.current_value_usd
                ratio = searchService.query_usd / value 
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
    .filter("cardEquivalent", ["searchService", "Currency", (searchService, Currency)->
            return (story)->
                return OSS.humanizeEquivalence story, {
                        currency: Currency.list[searchService.currency]
                        value:searchService.query_usd
                    }
                
        ]
    )