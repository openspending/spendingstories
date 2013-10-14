"use strict"

# Utililty toolbelt for our filters

OSS = OpenSpendingStories = window.SpendingStories = window.SpendingStories ||
    STORY_TYPES: 
        discrete:   'discrete'
        continous:  'over_one_year'

    RELEVANCE_TYPES: 
        equivalent: 'equivalent'
        half:       'half'
        multiple:   'multiple'
        percentage: 'percentage'
        week:       'weeks'
        month:      'months'
        day:        'days'

    getFloatPart: (value_f)->
        float_part_s = String(value_f).split('.')[1]
        return parseFloat([0,float_part_s].join('.'))

    getIntPart: (value_f)->
        return parseInt(String(value_f).split('.')[0])

    getDecimalNumber: (value_f, max_decimals=5)->
        return 0 unless value_f? and value_f isnt 0
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
        return null unless value?
        # Über rounding 
        Math.round(value * Math.pow(10, decimals))/Math.pow(10, decimals) 


    stupidPlural: (str, n)->
        result = str
        if n > 1
            result += 's'
        return result 

    humanize: (value, suffix, plural=false) ->
        return null unless value?
        # use it to humanize some amount and add a suffix (that can be 
        # pluralized if needed)
        if plural
            suffix += 's'
        if value < Math.pow(10, 6) || value > Math.pow(10, 15)
            Humanize.intcomma(value) + " " + suffix
        else
            Humanize.intword(value) + " " + suffix

    sentenceBuilder: (sentences, precision) ->
        # pick a sentence in a list of choices 
        s = _.find(sentences, (s)-> return precision >= s.precision[0] and precision < s.precision[1] ) or sentences[0]
        return s.value



    humanizeEquivalence: (story, query) ->
        return null unless story?
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
                equivalent = @humanizeEquivalent(story, query)
            when @RELEVANCE_TYPES.half
                equivalent = @humanizeHalf(story, query)
            when @RELEVANCE_TYPES.multiple
                equivalent = @humanizeMultiple(story, query)
            when @RELEVANCE_TYPES.percentage
                equivalent = @humanizePercentage(story, query)
            when @RELEVANCE_TYPES.month, @RELEVANCE_TYPES.week, @RELEVANCE_TYPES.day
                equivalent = @humanizeTime(story, query)
        console.log('humanizeEquivalent result:', equivalent,' from story: ', story)
        equivalent

    getRatioPrecision: (a, b) ->
        # return the absolute precision between `a` and `b` params 
        # returns float between 0 and 1.
        # 1 => absolutly precise, a = b
        # 0 => infinitly imprecise
        ratio = Math.abs(a - b) / b
        precision = 1 - ratio
        return precision

    humanizeEquivalent: (story, query) ->
        "an equivalent of"

    humanizeHalf: (story, query) ->
        if story.type is @STORY_TYPES.discrete
            equivalent = "50%"
        else 
            equivalent = "6 months"

        "≈ #{equivalent} of the"

    humanizeMultiple: (story, query) ->
        ratio = story.relevance_value
        "≈ #{ratio} times the"

    humanizePercentage: (story, query) ->
        ratio = story.relevance_value
        decimals = 1
        result = ratio
        if ratio >= 1 
            decimals = 0
        if ratio < 1
            decimals = OSS.getDecimalNumber(ratio)
            if decimals == 0
                decimals = 1
        result = OSS.round result, decimals
        if result < Math.pow(10,3)
            result = Humanize.intcomma(result, decimals)
        "≈ #{result}% of the"
    
    humanizeTime: (story, query) ->
        time_value = story.relevance_value
        console.log(@RELEVANCE_TYPES, story.relevance_type)
        switch story.relevance_type
            when @RELEVANCE_TYPES.month
                time_unit = "month"
            when @RELEVANCE_TYPES.week
                time_unit = "week"
            when @RELEVANCE_TYPES.day 
                time_unit = "day"

        story_value = story.current_value_usd
        equivalent = @stupidPlural("#{time_value} #{time_unit}", time_value)
        return "#{equivalent} of the"

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
                    return OSS.humanize(converted, _toCurrency.name, (converted > 1))
                else 
                    return ""
                
        ]
    )
    .filter("humanizeValue", ["Currency", (Currency)->
            return (value, currency="USD") ->
                return null unless angular.isNumber value
                _currency = Currency.list[currency]
                if _currency? then OSS.humanize value, _currency.name, value > 1 else "" 

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
                return "" unless d.current_value_usd?
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
                if story?
                    return OSS.humanizeEquivalence story, {
                            currency: Currency.list[searchService.currency]
                            value:searchService.query_usd
                        }
                else
                    return ""
                
        ]
    )