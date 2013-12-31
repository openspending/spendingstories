# ──────────────────────────────────────────────────────────────────────────────
# SearchService : utility service to search stories based on URL changes 
# ──────────────────────────────────────────────────────────────────────────────
class SearchService

    @$inject: ['$rootScope', '$location', 'Restangular', 'Currency']
    
    constructor: (@rootScope, @location, @Restangular, @Currency) ->
        # ──────────────────────────────────────────────────────────────────────
        # Constructor and instance's scope variables declaration 
        # ──────────────────────────────────────────────────────────────────────
        # Filter parameters accepted in URL, will produce filtering of stories 
        @accepted_filters = ['onlySticky', 'themes', 'country', 'currency', 'title', 'lang']

        @extra_fields = 
            ### 
            This attribute is used to bind some received URL parameters to some 
            extra API parameters. For example if the URL contains the parameters 
            "visualization" set "cards" it will request the API with an extra 
            parameter called`relevance_for` with the current @query_usd as 
            value.
            
            An exemple of binding 
              received_url = /#/search/?visualization=cards
              api_url      = /api/stories-nested/?relevance_for=@query_usd 
            
            ### 
            visualization:
                cards:
                    api_key: 'relevance_for'
                    instance_attr: 'query_usd'
        # current currency selected by user
        @currency  = 'USD'
        # current query entered by user 
        @query     = null
        # converted query value to USD 
        @query_usd = null
        # stories results will be holded in this attribute
        @results   = null
        
        init = =>
            @updateQuery @getURLParams(), ()=>
                @updateStories @getURLParams()


        @rootScope.$watch =>
                Currency.get(@getURLParams().c)
            , init
        # ──────────────────────────────────────────────────────────────────────
        # First initialization of instance attributes
        # ──────────────────────────────────────────────────────────────────────
        init()

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
        
    updateQuery: (params, cb = angular.noop)=>
        # will update instance variables & convert the query amount in USD if 
        # needed (currency != 'USD')
        # NOTE: theses changes may be optimised if we check changes 
        #       to avoid $digest        
        return if isNaN(parseInt(params.q))
        @query   = parseInt(params.q)
        currency = params.c || 'USD'
        # USD doesn't need convertion
        if currency is 'USD'
            @query_usd = @query 
            @currency  = currency
            do cb
        # Performs a USD convertion
        # The currency is already available
        else if @Currency.get(currency)?
            c = @Currency.get(currency)
            @currency = c.iso_code
            @query_usd = if c? then @query/c.rate else null
            do cb
        # NOTE: commented because get() doesn't provide a `then` method but an object.
        # The currency isn't loaded yet
        # else
        #     @Currency.get(currency).then (c)=>
        #         @currency = c.iso_code
        #         @query_usd = if c? then @query/c.rate else null
        #         do cb
    
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
            if field_meta?
                extra_api_params[field_meta.api_key] = @[field_meta.instance_attr] 
        return extra_api_params

    getFiltersParams: (params)=>
        # Extract the API filter parameters from the passed URL parameters 
        filters  = {}
        accepted = _.pick(params, @accepted_filters)
        for key, value of accepted 
            if value?
                if key == 'themes'
                    value = value.split(',')
                    filters[key] = value
                else if key == 'onlySticky'
                    if value == true
                        filters.sticky = 'True'
                    else
                        delete filters.sticky if filters.stick?
                else
                    filters[key] = value
        return filters

angular.module('storiesServices').service "searchService", SearchService