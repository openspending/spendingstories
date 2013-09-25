###
UBER CONSTANTS
### 
LITTERALS_SCALE = [
        value: 1e11
        str: "trillion"
    ,
        value: 1e9
        str: "billion"
    ,
        value: 1e6
        str: "million"
    ,
        value: 1e3
        str: "thousand"
    ,
        value: 1e2
        str: "hundred"
]

LITTERALS_UNIT = [
        value: 0
        str: "zero"
    ,
        value: 1
        str: "one"
    ,
        value: 2
        str: "two"
    ,
        value: 3
        str: "three"    
    ,
        value: 4
        str: "four"     
    ,
        value: 5
        str: "five"     
    ,
        value: 6
        str: "six"  
    ,
        value: 7
        str: "seven"    
    ,
        value: 8
        str: "eight"    
    ,
        value: 9
        str: "nine"     
    ,
        value: 10
        str: "ten"       
    ,
        value: 11
        str: "eleven"        
    ,
        value: 12
        str: "twelve"   
    ,
        value: 13
        str: "thirteen"
    ,
        value: 14
        str: "fourteen"
    ,
        value: 15
        str: "fifteen"  
    ,
        value: 16
        str: "sixteen"  
    ,
        value: 17
        str: "seventeen"    
    ,
        value: 18
        str: "eighteen"  
    ,
        value: 19
        str: "nineteen"
    ,
        value: 20
        str: "twenty"         
    ,
        value: 30
        str: "thirty"         
    ,
        value: 40
        str: "forty"          
    ,
        value: 50
        str: "fifty"          
    ,
        value: 60
        str: "sixty" 
    ,
        value: 70
        str: "seventy" 
    ,
        value: 80
        str: "eighty"  
    ,
        value: 90
        str: "ninety"
]

SEARCH_OPTS = 
    keys: ['str', 'value']
    id: 'value'
    treshold: 0.3

SEARCH_UNIT_SET  = new Fuse LITTERALS_UNIT, SEARCH_OPTS
SEARCH_SCALE_SET = new Fuse LITTERALS_SCALE, SEARCH_OPTS

class Comprehension
    @$inject : ['Currency']

    constructor : (@currency) ->
        @currency.list

    getPropositions : (query) =>
        #LowerCase the query for easier comparisons
        query = do query.toLowerCase

        #Initialize data structures
        currencies = []
        numbers = []
        propositions = []

        # [query, currencies] = matchCurrency query, @currency
        numbers   = matchNumbers query

        #Set defoult values if nothing was found
        currencies = (defaultCurrencies @currency) if currencies.length <= 0
        numbers = (do defaultNumbers) if numbers.length <= 0

        #Compute all numbers with all currencies
        currencies.map (currency) =>
            numbers.map (number) =>
                propositions.push
                    label : "#{number} #{currency[0]}"
                    currency : currency[1]
                    number : number
        # Finally return the propositions
        propositions
    
    matchNumbers = (query) =>
        splitArray = (array, pattern)->
            index_split = array.indexOf(pattern)
            if index_split isnt -1
                return [array.splice(0, index_split), array.splice(1, array.length - 1)]
            else
                return [array]

        searchValue = (term)->
            # perform a fuzzy search on our SEARCH sets
            parsed = parseInt(term)
            unless isNaN(parsed)
                return parsed
            else
                unit_results  = SEARCH_UNIT_SET.search(term)
                scale_results = SEARCH_SCALE_SET.search(term)
                unit_results[0] or scale_results[0]

        processTerms = (terms)->
            # will convert one and/or number arrays to a JS number 
            if terms.length is 0
                return 0
            # perform fuzzy search (@see searchValue) on every element and do an addition
            numbers = _.map terms, (t)-> _.reduce(_.map(t.split('-'), searchValue), (e,sum)-> return e + sum) 
            sum = _.reduce numbers, (w, sum)-> sum *= w

        matched = {}
        words = query.split(/\s+/)
        splitted_array = splitArray(words, 'and')
        sum = _.reduce splitted_array, (memo, words)->
                return memo + processTerms(words)
            , 0

        [sum, sum * 10, sum * 100]

    matchCurrency = (query, currency) =>
        matched = {}
        words = query.split /\s+/
        max = 0
        strippedQuerry = query

        for iso, curr of currency.list
            name = do curr.name.toLowerCase
            #Match ISO codes
            if query.match do iso.toLowerCase
                strippedQuerry = strippedQuerry.replace do iso.toLowerCase, ''
                matched[iso] = [curr.name]
            #Or do a word comparison
            else
                num = 0
                words.map (word) =>
                    if name.match word
                        ++num
                        matched[iso] = [curr.name, num]
                        strippedQuerry = strippedQuerry.replace word, ''
                max = num if num > max

        #Keep only the best matches
        matches = []
        for iso, curr of matched
            if not curr[1]? or curr[1] is max
                matches.push [curr[0], iso]

        #Finally return the new query and the matches
        [strippedQuerry, matches]

    defaultCurrencies = (currency) =>
        ['USD', 'EUR', 'GBP'].map (iso) -> [currency.list[iso].name, iso]

    defaultNumbers = () =>
        [100000]

angular.module('storiesServices').service "comprehensionService", Comprehension