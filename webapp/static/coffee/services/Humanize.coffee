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


    humanize: (value, suffix, plural=false)=>
        return null unless value?
        # use it to humanize some amount and add a suffix (that can be 
        # pluralized if needed)
        if plural
            suffix += 's'
        if value < Math.pow(10, 6) || value > Math.pow(10, 15)
            Humanize.intcomma(value) + " " + suffix
        else
            Humanize.intword(value) + " " + suffix

    humanizeEquivalence: (story, query)=>
        return null unless story?
        value = story.relevance_value
        switch story.relevance_type
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
                equivalent = @humanizeTime(value)
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
        multiple_wording = @$translate('HUMANIZE_MULTIPLE', {value: value})
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
            result = Humanize.intcomma(result, decimals)

        word_end = @$translate('HUMANIZE_OF_THE')
        "≈ #{result}% #{word_end}"
    
    humanizeTime: (value, type)=>
        # Please don't refactor
        switch type
            when @RELEVANCE_TYPES.month
                time_unit_translated = @$translate("HUMANIZE_MONTH", { value: value })
            when @RELEVANCE_TYPES.week
                time_unit_translated = @$translate("HUMANIZE_WEEK" , { value: value })
            when @RELEVANCE_TYPES.day 
                time_unit_translated = @$translate("HUMANIZE_DAY"  , { value: value })
        word_end = @$translate('HUMANIZE_OF_THE')
        "#{value} #{time_unit_translated} #{word_end}"


angular.module('storiesServices').service "humanizeService", HumanizeService
