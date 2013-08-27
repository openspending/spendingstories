class SearchService
    @$inject: ['Restangular', 'Currency']
    constructor: (@Restangular, @Currency) ->
        @currency      = 'USD'
        @query         =  null
        @query_usd     =  null
        @stories       =  @Restangular.all('stories-nested')
        @results       =  this.stories.getList()
        @filter_fields = 
            'sticky': {
                'type': typeof true
            }
            'country': {
                'type': typeof ""
            }
            'currency': {
                'type': typeof ""
            }
            'themes': {
                'type': typeof []
            }

        @accepted_filters = _.keys(@filter_fields)

    set: (params) =>
        @filterStories(params)
        query = params.q
        currency = params.c || 'USD'
        # USD doesn't need convertion
        if currency is 'USD'
            @currency  = currency                      
            @query     = query
            @query_usd = query    
        # Performs a USD convertion
        # The currency is already available
        else if @Currency.list[currency]?
            c = @Currency.list[currency]
            @query    = query
            @currency = c.iso_code                    
            @query_usd = if c? then query/c.rate else null
        # The currency isn't loaded yet
        else
            @Currency.get(currency).then (c)->
                @query    = query
                @currency = c.iso_code                    
                @query_usd = if c? then query/c.rate else null

    filterStories: (params)=>
        filters    = {}
        params     = _.pick(params, @accepted_filters)
        filters[k] = @processParam(k, param) for k,param of params
        console.log 'params:', filters 
        @results   = @stories.getList(filters)


    processParam: (field_key, param)=>
        processed = param
        field_type = @filter_fields[field_key].type
        if field_type == typeof true
            processed = @processBooleanParam(param)
        return processed


    processBooleanParam: (param)=>
        """
        Convert a (string|boolean) `param` to string. 
        This string represent a python boolean (e.g: True, False)
        """
        # dumbydumb bool conversion
        param = param.toLowerCase() is "true" ? true : false 
        # Yes, we convert back to string but now we are sure to deal with a 
        # boolean (true or false), we limit side-effects this way. 
        param = ""+param
        return  param[0].toUpperCase() + param.slice(1)



angular.module('storiesServices')
    # Create a factory dedicated to research
    .service "searchService", SearchService