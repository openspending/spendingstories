class SearchService
    @$inject: ['Restangular', 'Currency']
    
    constructor: (@Restangular, @Currency) ->
        @currency  = 'USD'
        @query     =  null
        @query_usd =  null
        @results   =  @Restangular.all('stories-nested').getList()
        # filters fields for stories and their process functions 
        @accepted_filters = ['onlySticky', 'themes', 'country', 'currency']


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

    set: (params) =>
        # process the passed HTTP params to get the filters 
        filters_params = @getFiltersParams(params)
        # we need to keep the old reference of @results in order to propagate 
        # changes around the application when @results changes (e.g: when we 
        # filter them for instance)
        @results   = @Restangular.copy(@results)
        # then we filter the stories with the passed parameters
        @results = @Restangular.all('stories-nested').getList(filters_params)
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

angular.module('storiesServices')
    # Create a factory dedicated to research
    .service "searchService", SearchService