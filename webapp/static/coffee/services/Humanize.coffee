number_format = (number, decimals, dec_point, thousands_sep) =>
    # http://kevin.vanzonneveld.net
    # +   original by: Jonas Raoni Soares Silva (http://www.jsfromhell.com)
    # +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    # +     bugfix by: Michael White (http://crestidg.com)
    # +     bugfix by: Benjamin Lupton
    # +     bugfix by: Allan Jensen (http://www.winternet.no)
    # +    revised by: Jonas Raoni Soares Silva (http://www.jsfromhell.com)    
    # *     example 1: number_format(1234.5678, 2, '.', '');
    # *     returns 1: 1234.57  
    n = number
    c = (if isNaN(decimals = Math.abs(decimals)) then 2 else decimals)
    d = (if dec_point is `undefined` then "," else dec_point)
    t = (if thousands_sep is `undefined` then "." else thousands_sep)
    s = (if n < 0 then "-" else "")
    i = parseInt(n = Math.abs(+n or 0).toFixed(c)) + ""
    j = (if (j = i.length) > 3 then j % 3 else 0)
    s + ((if j then i.substr(0, j) + t else "")) + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + ((if c then d + Math.abs(n - i).toFixed(c).slice(2) else ""))

# Utililty toolbelt for our filters
class HumanizeService
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

    @$inject: ['$translate']

    constructor:(@$translate)->

    intcomma:(number, decimals) =>
        ###
        Took from [JS-Humanize](https://github.com/milanvrekic/JS-humanize)
        Converts an integer to a string containing commas every three digits.

        Examples:

            4500 becomes 4,500.
            45000 becomes 45,000.
            450000 becomes 450,000.
            4500000 becomes 4,500,000.
        ###
        decimals = (if decimals is `undefined` then 0 else decimals)
        number_format number, decimals, @$translate('HUMANIZE_DECIMAL_SEP'), @$translate('HUMANIZE_THOUSAND_SEP')



    intword: (number) =>
        ###
        Took from [Humanize.js](https://github.com/milanvrekic/JS-humanize)
        Converts a large integer to a friendly text representation. Works best for numbers over 1 million.

        Examples:
        1000000 becomes 1.0 million.
        1200000 becomes 1.2 million.
        1200000000 becomes 1.2 billion.
        ### 
        number = parseInt(number)
        if number < 1000000
            return number
        else if number < 100
            return @intcomma(number, 1)
        else if number < 1000
            final_number = number / 100
            wording = @pluralize value: final_number, single: @$translate('HUNDRED'), plural: @$translate('HUNDRED_PLURAL')  
            return "#{@intcomma(final_number, 1)} #{wording}"

        else if number < 100000
            final_number = number / 1000.0
            wording = @pluralize value: final_number, single: @$translate('THOUSAND') , plural: @$translate('THOUSAND_PLURAL')
            return "#{@intcomma(final_number, 1)} #{wording}"

        else if number < 1000000
            final_number = number / 100000.0
            hundred  = @pluralize value: final_number, single: @$translate('HUNDRED'), plural: @$translate('HUNDRED_PLURAL')
            return "#{@intcomma(final_number, 1)} #{hundred} #{@$translate('THOUSAND_PLURAL')}"

        else if number < 1000000000
            final_number = number / 1000000.0
            wording = @pluralize value: final_number, single: @$translate('MILLION'), plural: @$translate('MILLION_PLURAL')
            return "#{@intcomma(final_number, 1)} #{wording}"

        else if number < 1000000000000 #senseless on a 32 bit system probably.
            final_number = number / 1000000000.0
            wording = @pluralize value: final_number, single: @$translate('BILLION'), plural: @$translate('BILLION_PLURAL')
            return "#{@intcomma(final_number, 1)} #{wording}"

        else if number < 1000000000000000
            final_number = number / 1000000000000.0
            wording = @pluralize value: final_number, single: @$translate('TRILLION'), plural: @$translate('TRILLION_PLURAL')
            return "#{@intcomma(final_number, 1)} #{wording}"
        else
            return "" + number # too big.

    getFloatPart: (value_f)=>
        float_part_s = String(value_f).split('.')[1]
        return parseFloat([0,float_part_s].join('.'))

    getIntPart: (value_f)=>
        return parseInt(String(value_f).split('.')[0])

    getDecimalNumber: (value_f, max_decimals=5)=>
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

    round: (value, decimals=2)=>
        return null unless value?
        # Über rounding 
        Math.round(value * Math.pow(10, decimals))/Math.pow(10, decimals) 

    pluralize: (opts)=>
        is_plural = (value)=>
            limit = parseInt(@$translate('PLURAL_LIMIT')) or 1
            if limit is 1
                return value > limit
            else
                return value >= limit
        if is_plural(opts.value) then (opts.plural or opts.single + 's') else opts.single

    humanizeValue: (value, suffix, pluralizeSuffix=true)=>
        return null unless value?
        if pluralizeSuffix
            # use it to humanize some amount and add a suffix (that can be 
            suffix = @pluralize value: value, single: suffix
        
        use_wording = value >= Math.pow(10, 6) and value <= Math.pow(10, 15)
        # pluralized if needed)
        if use_wording
            wording = @intword(value)
        else
            if value < 1
                wording = value
            else
                wording = @intcomma(value)
        union_word = @$translate('HUMANIZE_CURRENCY_UNION_WORD')
        unless _.isEmpty(union_word) or !use_wording
            union = " #{union_word} "
        else
            union = ' '

        "#{wording}#{union}#{suffix}"
        

    humanizeEquivalence: (story, query)=>
        return null unless story?
        value = story.relevance_value
        type  = story.relevance_type
        switch type
            when @RELEVANCE_TYPES.equivalent
                equivalent = @humanizeEquivalent(value)
            when @RELEVANCE_TYPES.half
                if story.type is @STORY_TYPES.discrete
                    equivalent = @humanizePercentage(50)
                else
                    equivalent = @humanizeTime(6, @RELEVANCE_TYPES.month)
            when @RELEVANCE_TYPES.multiple
                equivalent = @humanizeMultiple(value)
            when @RELEVANCE_TYPES.percentage
                equivalent = @humanizePercentage(value)
            when @RELEVANCE_TYPES.month, @RELEVANCE_TYPES.week, @RELEVANCE_TYPES.day
                equivalent = @humanizeTime(value, type)
        equivalent

    getRatioPrecision: (a, b)=>
        # return the absolute precision between `a` and `b` params 
        # returns float between 0 and 1.
        # 1 => absolutly precise, a = b
        # 0 => infinitly imprecise
        ratio = Math.abs(a - b) / b
        precision = 1 - ratio
        return precision

    humanizeEquivalent: (story)=>
        @$translate("HUMANIZE_EQUIVALENT")

    humanizeMultiple: (value) =>
        multiple_wording = @pluralize({ value: value, single: @$translate("HUMANIZE_MULTIPLE"), plural: @$translate("HUMANIZE_MULTIPLE_PLURAL")})
        "≈ #{value} #{multiple_wording}"

    humanizePercentage: (value)=>
        decimals = 1
        result = value
        if value >= 1 
            decimals = 0
        if value < 1
            decimals = @getDecimalNumber(value)
            if decimals == 0
                decimals = 1
        result = @round result, decimals
        if result < Math.pow(10,3)
            result = @intcomma(result, decimals)

        word_end = @$translate('HUMANIZE_OF_THE')
        "≈ #{result}% #{word_end}"
    
    humanizeTime: (value, type)=>
        # Please don't refactor
        switch type
            when @RELEVANCE_TYPES.month
                time_unit_translated = @pluralize({ value: value, single: @$translate("HUMANIZE_MONTH"), plural: @$translate("HUMANIZE_MONTHS") })
            when @RELEVANCE_TYPES.week
                time_unit_translated = @pluralize({ value: value, single: @$translate("HUMANIZE_WEEK"),  plural: @$translate("HUMANIZE_WEEKS")  })
            when @RELEVANCE_TYPES.day 
                time_unit_translated = @pluralize({ value: value, single: @$translate("HUMANIZE_DAY"),   plural: @$translate("HUMANIZE_DAYS")   })
        
        word_end = @$translate('HUMANIZE_OF_THE')
        "#{value} #{time_unit_translated} #{word_end}"


angular.module('storiesServices').service "humanizeService", HumanizeService
