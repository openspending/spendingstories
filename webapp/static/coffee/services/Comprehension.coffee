TYPES = {
    number: 'number'
    currency: 'currency'
}

# Search set is the set who will be used for fuzzy searching values.
# It regroups currencies and numbers to get the most relevant result for each
# search term

SEARCH_SET_DATA = [
        id: 0
        value: 0
        name: "zero"
        type: TYPES.number
    ,
        id: 1
        value: 1
        name: "one"
        type: TYPES.number
    ,
        id: 2
        value: 2
        name: "two"
        type: TYPES.number
    ,
        id: 3
        value: 3
        name: "three"
        type: TYPES.number
    ,
        id: 4
        value: 4
        name: "four"
        type: TYPES.number
    ,
        id: 5
        value: 5
        name: "five"
        type: TYPES.number
    ,
        id: 6
        value: 6
        name: "six"
        type: TYPES.number
    ,
        id: 7
        value: 7
        name: "seven"
        type: TYPES.number
    ,
        id: 8
        value: 8
        name: "eight"
        type: TYPES.number
    ,
        id: 9
        value: 9
        name: "nine"
        type: TYPES.number
    ,
        id: 10
        value: 10
        name: "ten"
        type: TYPES.number
    ,
        id: 11
        value: 11
        name: "eleven"
        type: TYPES.number
    ,
        id: 12
        value: 12
        name: "twelve"
        type: TYPES.number
    ,
        id: 13
        value: 13
        name: "thirteen"
        type: TYPES.number
    ,
        id: 14
        value: 14
        name: "fourteen"
        type: TYPES.number
    ,
        id: 15
        value: 15
        name: "fifteen"
        type: TYPES.number
    ,
        id: 16
        value: 16
        name: "sixteen"
        type: TYPES.number
    ,
        id: 17
        value: 17
        name: "seventeen"
        type: TYPES.number
    ,
        id: 18
        value: 18
        name: "eighteen"
        type: TYPES.number
    ,
        id: 19
        value: 19
        name: "nineteen"
        type: TYPES.number
    ,
        id: 20
        value: 20
        name: "twenty"
        type: TYPES.number
    ,
        id: 21
        value: 30
        name: "thirty"
        type: TYPES.number
    ,
        id: 22
        value: 40
        name: "forty"
        type: TYPES.number
    ,
        id: 23
        value: 50
        name: "fifty"
        type: TYPES.number
    ,
        id: 24
        value: 60
        name: "sixty"
        type: TYPES.number
    ,
        id: 25
        value: 70
        name: "seventy"
        type: TYPES.number
    ,
        id: 26
        value: 80
        name: "eighty"
        type: TYPES.number
    ,
        id: 27
        value: 90
        name: "ninety"
        type: TYPES.number
    ,
        id: 28
        value: 1e2
        name: "hundred"
        type: TYPES.number
    ,
        id: 29
        value: 1e3
        name: "thousand"
        type: TYPES.number
    ,
        id: 30
        value: 1e6
        name: "million"
        type: TYPES.number
    ,
        id: 31
        value: 1e9
        name: "billion"
        type: TYPES.number
    ,
        id: 32
        value: 1e11
        name: "trillion"
        type: TYPES.number
    ,
        id: 33
        value: 'EUR'
        symbol: '€'
        name: 'Euro'
        type: TYPES.currency
    ,
        id: 33
        value: 'GBP'
        symbol: '£'
        name: 'British Pound'
        type: TYPES.currency
    ,
        id: 33
        value: 'USD'
        symbol: '$'
        name: 'US Dollar'
        type: TYPES.currency
]

DECIMAL_CARACTER = {
    'fr': ','
    'en': '.'
}

SEARCH_OPTS =
    keys: ['name', 'value', 'symbol']
    treshold: 0.3

class Comprehension
    @$inject : ['$window', 'Currency']

    constructor : ($window, @currency) ->
        # when currencies will be filtered:
        # add currencies to SEARCH_SET_DATA with format:
        # {value: <iso code>, symbol: <unicode symbol>, name: <full currency name }
        @searchSet = new Fuse SEARCH_SET_DATA, SEARCH_OPTS
        @language  = ($window.navigator.userLanguage || $window.navigator.language).substr(0, 2)

        @local_decimal_caracter = DECIMAL_CARACTER[@language] or DECIMAL_CARACTER['en']

    getPropositions : (query) =>
        #LowerCase the query for easier comparisons
        @original_query = query
        @query = do query.toLowerCase

        #Initialize data structures
        currencies = []
        numbers = []
        propositions = []

        # First step: extract numbers from query (query is changed)
        [numbers, @query] = @extractNumbers @query
        terms = _.groupBy (_.flatten _.map atomize(@query), @searchValue), 'type'

        currencies = matchCurrency query, @currency
        numbers   = matchNumbers query

        #Set defoult values if nothing was found
        currencies = (defaultCurrencies @currency) if currencies.length <= 0
        numbers = (do defaultNumbers) if numbers.length <= 0

        #Compute all numbers with all currencies
        _.map currencies, (currency) =>
            _.map numbers, (number) =>
                propositions.push
                    label : "#{number} #{currency[0]}"
                    currency : currency[1]
                    number : number
        # Finally return the propositions
        propositions

    extractNumbers: (query) =>
        query_numbers = query.match(/\d{1,3}([,|\.]?\s*\d{1,3})*/g)
        numbers = undefined
        if query_numbers?
            numbers = for number in query_numbers
                do()=>
                    query.replace(number, '')
                    number =
                        index: @getTermPosition(number)
                        value: parseNumber(number)
                        type:  TYPES.number
        return [numbers, query]

    parseNumber = (str_number)->
        number = str_number.split(@local_decimal_caracter)
        sub_numbers = number[0].match(/\d+/g)

        if sub_numbers? then n = sub_numbers.join('') else n = str_number
        return parseInt(n)

    getTermPosition: (term)=>
        return @original_query.indexOf(term)

    atomize = (str)=>
        str.split(/[\s+|-]/)

    searchValue: (term)=>
        _.map ([_.first @searchSet.search term]), (elem) =>
            _.extend elem,
                index : @getTermPosition term
                term : term

    matchNumbers = (query) =>
        splitArray = (array, pattern)->
            index_split = array.indexOf(pattern)
            if index_split isnt -1
                return [array.splice(0, index_split), array.splice(1, array.length - 1)]
            else
                return [array]

        searchValue = (term, index, list)->

        processTerms = (terms)->
            # will convert one and/or number arrays to a JS number
            if terms.length is 0
                return 0
            # perform fuzzy search (@see searchValue) on every element and do an addition
            numbers = _.map terms, searchValue 
            sum = _.reduce numbers, (memo, sum)->
                    if sum.type is LITTERALS_TYPES.unit
                        value = memo + (sum.value or 0)
                    else 
                        value = memo * (sum.value or 1)
                    return value
                , 0

            if _.isObject sum 
                return sum.value
            else
                return sum

        matched = {}
        words = query.split(/\s+/)
        splitted_array = splitArray(words, 'and')
        sum = _.reduce splitted_array, (memo, words)->
                return memo + processTerms(words)
            , 0

        [sum, sum * 10, sum * 100]

    matchCurrency = (query, currency) =>
        currencies = []
        for key, value of currency.list
            currencies.push
                iso : key
                name : value.name

        #Keep exactly matched ISO codes
        words = query.split(/\s+/)
        matches = []
        _.map words, (word) =>
            _.map currencies, (curr) =>
                if (do curr.iso.toLowerCase) is word
                    matches.push [curr.name, curr.iso]

        #Fuzzy search !
        options =
            keys : ['iso', 'name']
        matched = (new Fuse currencies, options).search query

        #Finally return the matches
        _.union matches, _.map matched, (match) =>
            [match.name, match.iso]

    defaultCurrencies = (currency) =>
        _.map ['USD', 'EUR', 'GBP'], (iso) -> [currency.list[iso].name, iso]

    defaultNumbers = () =>
        [100000]

angular.module('storiesServices').service "comprehensionService", Comprehension