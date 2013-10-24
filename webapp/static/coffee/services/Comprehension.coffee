TYPES = {
    number: 'number'
    currency: 'currency'
}

SEARCH_OPTS =
    keys: ['name', 'value', 'symbol']
    treshold: 0.3

class Comprehension
    @$inject: ['$translate', '$rootScope', 'Currency']

    constructor: (@$translate, @rootScope, @currency) ->
        @search_set_data = []
        @rootScope.$watch ()=>
                @$translate.uses()
            , (newVal, oldVal)=>
                return unless newVal?
                @search_set_data = @getSearchSet()
                @local_decimal_caracter = @$translate('HUMANIZE_DECIMAL_SEP')

                (do @currency.all.getList).then (data) =>
                    _.map data, (curr) =>
                        @search_set_data.push
                            value : curr.iso_code
                            symbol : curr.symbol
                            name : curr.name
                            type : TYPES.currency
                            priority : curr.priority
                    @searchSet = new Fuse @search_set_data, SEARCH_OPTS

    getPropositions: (query) =>
        #LowerCase the query for easier comparisons
        @original_query = query
        @query = do query.toLowerCase

        #Initialize data structures
        currencies = []
        numbers = []
        propositions = []

        # First step: extract numbers from query (query is changed)
        [query_numbers, @query] = @extractNumbersFromQuery @query
        terms = _.map atomize(@query), @searchValue if @query isnt ""
        if terms?
            terms = _.groupBy(_.flatten(terms), 'type')
            number_terms = terms[TYPES.number] || []
            number_terms = number_terms.concat(query_numbers) if query_numbers?
            number_terms = _.sortBy(number_terms, (term)-> term.index )
            terms[TYPES.number] = number_terms
        else
            terms =
                'number': query_numbers if query_numbers

        numbers    = @extractNumbersFromTerms(terms[TYPES.number])

        counts = _.countBy terms[TYPES.currency], 'name'
        currencies = _.map (_.uniq terms[TYPES.currency]), (c) =>
            _.extend c, _priority : c.priority - counts[c.name]
        currencies = _.first (_.sortBy currencies, '_priority'), 3

        #Set default values if nothing was found
        currencies = (defaultCurrencies @currency) if not currencies? or currencies.length <= 0
        numbers = (do defaultNumbers) if not numbers? or numbers.length <= 0

        #Compute all numbers with all currencies
        _.map currencies, (currency) =>
            _.map numbers, (number) =>
                propositions.push
                    currency : currency.value
                    number : number
        # Finally return the propositions
        propositions

    extractNumbersFromQuery: (query) =>
        query_numbers = query.match(/\d{1,3}([,|\.]?\s*\d{1,3})*/g)
        numbers = undefined
        if query_numbers?
            numbers = for number in query_numbers
                do()=>
                    query  = query.replace(number, '')
                    return {
                        index: @getTermPosition(number)
                        value: parseNumber(number)
                        type:  TYPES.number
                    }
        return [numbers, query]

    extractNumbersFromTerms: (terms) =>
        sum = _.reduce(terms, (memo, term)->
                return term.value if memo is 0
                if term.value > memo
                    return (memo or 1) * (term.value or 1)
                else
                    return (memo or 0) + (term.value or 0)
            , 0 )
        if sum > 0 then [sum] else undefined

    parseNumber = (str_number)->
        number = str_number.split(@local_decimal_caracter)
        sub_numbers = number[0].match(/\d+/g)
        if sub_numbers? then n = sub_numbers.join('') else n = str_number
        return parseInt(n)

    getTermPosition: (term)=>
        return @original_query.indexOf(term)

    atomize = (str)=>
        _.without(str.split(/[\s+|-]/), '', 'and', '+' , '.', ',')

    searchValue: (term)=>
        results = _.map (@searchSet.search term), (elem) =>
            _.extend elem,
                index : @getTermPosition term
                term : term
        if results[0].type is TYPES.number
            return _.first results
        else
            _.filter results, (result) -> result.type is TYPES.currency

    defaultCurrencies = (currency) =>
        _.map ['USD', 'EUR', 'GBP'], (iso) ->
            name : currency.list[iso].name
            value : iso

    defaultNumbers = () =>
        [100000]

    getSearchSetData: ()=>
        # Search set is the set who will be used for fuzzy searching values.
        # It regroups currencies and numbers to get the most relevant result for each
        # search term
        SEARCH_SET_DATA = [
                id: 0
                value: 0
                name: @$translate("ZERO")
                type: TYPES.number
            ,
                id: 1
                value: 1
                name: @$translate("ONE")
                type: TYPES.number
            ,
                id: 2
                value: 2
                name: @$translate("TWO")
                type: TYPES.number
            ,
                id: 3
                value: 3
                name: @$translate("THREE")
                type: TYPES.number
            ,
                id: 4
                value: 4
                name: @$translate("FOUR")
                type: TYPES.number
            ,
                id: 5
                value: 5
                name: @$translate("FIVE")
                type: TYPES.number
            ,
                id: 6
                value: 6
                name: @$translate("SIX")
                type: TYPES.number
            ,
                id: 7
                value: 7
                name: @$translate("SEVEN")
                type: TYPES.number
            ,
                id: 8
                value: 8
                name: @$translate("EIGHT")
                type: TYPES.number
            ,
                id: 9
                value: 9
                name: @$translate("NINE")
                type: TYPES.number
            ,
                id: 10
                value: 10
                name: @$translate("TEN")
                type: TYPES.number
            ,
                id: 11
                value: 11
                name: @$translate("ELEVEN")
                type: TYPES.number
            ,
                id: 12
                value: 12
                name: @$translate("TWELVE")
                type: TYPES.number
            ,
                id: 13
                value: 13
                name: @$translate("THIRTEEN")
                type: TYPES.number
            ,
                id: 14
                value: 14
                name: @$translate("FOURTEEN")
                type: TYPES.number
            ,
                id: 15
                value: 15
                name: @$translate("FIFTEEN")
                type: TYPES.number
            ,
                id: 16
                value: 16
                name: @$translate("SIXTEEN")
                type: TYPES.number
            ,
                id: 17
                value: 17
                name: @$translate("SEVENTEEN")
                type: TYPES.number
            ,
                id: 18
                value: 18
                name: @$translate("EIGHTEEN")
                type: TYPES.number
            ,
                id: 19
                value: 19
                name: @$translate("NINETEEN")
                type: TYPES.number
            ,
                id: 20
                value: 20
                name: @$translate("TWENTY")
                type: TYPES.number
            ,
                id: 21
                value: 30
                name: @$translate("THIRTY")
                type: TYPES.number
            ,
                id: 22
                value: 40
                name: @$translate("FORTY")
                type: TYPES.number
            ,
                id: 23
                value: 50
                name: @$translate("FIFTY")
                type: TYPES.number
            ,
                id: 24
                value: 60
                name: @$translate("SIXTY")
                type: TYPES.number
            ,
                id: 25
                value: 70
                name: @$translate("SEVENTY")
                type: TYPES.number
            ,
                id: 26
                value: 80
                name: @$translate("EIGHTY")
                type: TYPES.number
            ,
                id: 27
                value: 90
                name: @$translate("NINETY")
                type: TYPES.number
            ,
                id: 28
                value: 1e2
                name: @$translate("HUNDRED")
                type: TYPES.number
            ,
                id: 29
                value: 1e3
                name: @$translate("THOUSAND")
                type: TYPES.number
            ,
                id: 30
                value: 1e6
                name: @$translate("MILLION")
                type: TYPES.number
            ,
                id: 31
                value: 1e9
                name: @$translate("BILLION")
                type: TYPES.number
            ,
                id: 32
                value: 1e12
                name: @$translate("TRILLION")
                type: TYPES.number
        ]
        _.filter SEARCH_SET_DATA, (s)-> !_.isEmpty(s.name)

angular.module('storiesServices').service "comprehensionService", Comprehension