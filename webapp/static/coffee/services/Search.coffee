# ──────────────────────────────────────────────────────────────────────────────
# SearchService : utility service to search stories based on URL changes 
# ──────────────────────────────────────────────────────────────────────────────
class SearchService

    @$inject: ['$rootScope', '$location', 'Restangular', 'Currency']
    
    constructor: (@rootScope, @location, @Restangular, @Currency) ->
        # ──────────────────────────────────────────────────────────────────────
        # Constructor and instance's scope variables declaration 
        # ──────────────────────────────────────────────────────────────────────
        searchParams = @location.search()
        # Filter parameters accepted in URL, will filter the stories 
        @accepted_filters = ['onlySticky', 'themes', 'country', 'currency']
        # These fields are used to bind some params in URL to some params in API
        # values are retrieved from the searchService instance, for example
        @extra_fields =
            visualization:
                # For cards mode we want to get the stories sorted by 
                # relevance, see wiki for this relevance model
                cards:
                    # Will request the API with relevance_for parameters
                    api_key: 'relevance_for'
                    # and with the instance attribute `query_usd` as value
                    # /api/stories-nested/?relevance_for=@query_usd 
                    instance_attribute: 'query_usd'
        # current currency selected by user
        @currency  = 'USD'
        # current query entered by user 
        @query     = null
        # converted query value to USD 
        @query_usd = null
        # stories results will be holded in this attribute
        @results   = null

        # ──────────────────────────────────────────────────────────────────────
        # First initialization of instance attributes
        # ──────────────────────────────────────────────────────────────────────
        @updateStories(searchParams)
        @updateQuery(searchParams)

        # ──────────────────────────────────────────────────────────────────────
        # Watchers
        # ──────────────────────────────────────────────────────────────────────
        # binding for URL changes 
        @rootScope.$watch @getURLParams, @onURLChanged, true

    getURLParams: =>
        # returns the URL parameters as javascript object
        @location.search()

    onURLChanged: () =>
        # when URL change we want to update the stories in consequence 
        params = @location.search()
        @updateQuery(params)
        @updateStories(params)
        
    updateQuery: (params)=>
        # will update instance variables & convert the query amount in USD if 
        # needed (currency != 'USD')
        # NOTE: theses changes may be optimised if we check changes 
        #       to avoid $digest
        @query   = parseInt(params.q)
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
    
    updateStories: (params)=>
        # will fire a new request on API with the new paramters
        @results = @Restangular.copy(@results) if @results?
        @results = @Restangular.all('stories-nested').getList(@getAPIParams(params))
     
    getAPIParams: (newParams)=>
        # extract the parameters from URL that will be used to request the API
        _.extend(@getFiltersParams(newParams), @getExtraParams(newParams))
    
    getExtraParams: (newParams)=>
        # does the binding between URL parameters and some extra field to add to
        # API parameters 
        extra_api_params = {}
        accepted = _.pick(newParams, _.keys(@extra_fields)) 
        _.each accepted, (value, key)=>
            field_meta = @extra_fields[key][value]
            extra_api_params[field_meta.api_key] = @[field_meta.value_key] if field_meta?
        return extra_api_params

    getFiltersParams: (params)=>
        # Extract the API filter parameters from the passed URL parameters 
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

angular.module('storiesServices').service "searchService", SearchService