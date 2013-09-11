class SearchService
    ### 
    SearchService : utility service to search results based on URL changes 
    ### 

    @$inject: ['$rootScope', '$location', 'Restangular', 'Currency']
    
    constructor: (@rootScope, @location, @Restangular, @Currency) ->
        searchParams = @location.search()
        @accepted_filters = ['onlySticky', 'themes', 'country', 'currency']
        @extra_fields = {
            visualisation: {
                cards: {
                    api_key: 'relevance_for'
                    value_key: 'query_usd'
                }
            }
        }
        @currency  = 'USD'
        @query     = null
        @query_usd = null
        @results   = null 
        @updateAPIParams(searchParams)
        @updateQuery(searchParams)

        # binding for URL changes 
        @rootScope.$watch @getURLParams, @onURLChanged, true

    getURLParams: =>
        @location.search()

    updateQuery: (params)=>
         # may be optimised if we check changes to avoid $digest
        @query   = parseInt(params.q)
        console.log "query is updated by", @query
        currency = params.c || 'USD'
        # USD doesn't need convertion
        if currency is 'USD'
            @query_usd = @query 
            @currency  = currency
        # Performs a USD convertion
        # The currency is already available
        else if @Currency.list[currency]?
            c = @Currency.list[currency]
            @currency = c.iso_code
            @query_usd = if c? then @query/c.rate else null
        # The currency isn't loaded yet
        else
            @Currency.get(currency).then (c)->
                @currency = c.iso_code
                @query_usd = if c? then @query/c.rate else null
    
    updateAPIParams: (params)=>
        @results = @Restangular.copy(@results) if @results?
        @results = @Restangular.all('stories-nested').getList(@getAPIParams(params))

    
    onURLChanged: () =>
        console.log "URL Changed !"
        params = @location.search()
        @updateQuery(params)
        @updateAPIParams(params)
     
    paramsChanged: (params)=>
        _.find(params, @hasChanged)?

    hasChanged: (value, key)=>
        !@apiParams? || !@apiParams[key]? || value != @apiParams[key]

    getAPIParams: (newParams)=>
        _.extend(@getFiltersParams(newParams), @getExtraParams(newParams))
    
    getExtraParams: (newParams)=>
        extra_api_params = {}
        accepted = _.pick(newParams, _.keys(@extra_fields)) 
        _.each accepted, (value, key)=>
            field_meta = @extra_fields[key]
            extra_api_params[field_meta.api_key] = @[field_meta.value_key]

        return extra_api_params

    getFiltersParams: (params)=>
        filters  = {}
        accepted = _.pick(params, @accepted_filters)
        for key, value of accepted 
            do()->
                if value?
                    if key == 'onlySticky'
                        if value == true
                            filters.sticky = 'True'
                        else
                            delete filters.sticky if filters.stick?
                    else
                        filters[key] = value
        return filters

angular.module('storiesServices')
    # Create a factory dedicated to research
    .service "searchService", SearchService