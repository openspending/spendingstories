class FilterCtrl
    @$inject: ['$scope', '$routeParams', '$location', 'Currency', 'Restangular']
    constructor: (@scope, @routeParams, @location, Currency, Restangular)->
        @searchParams = @location.search()
        @scope.filters = {
            onlySticky:
                stackable: false
                type: 'boolean'
                value: @searchParams.onlySticky
            country:
                type: 'string'
                stackable: true 
                value: @searchParams.country
                activated: @searchParams.country?
            currency:
                type: 'string'
                stackable: true
                value: @searchParams.currency
                activated: @searchParams.currency?
            themes:
                type: 'array'
                stackable: false
                value: if @searchParams.themes? then @searchParams.themes.split(',')
                activated: @searchParams.themes?


        }

        # Not handled for the moment
        # type:       if @searchParams.type?       then @searchParams.type
        @scope.currency_list = Currency.list
        @scope.country_list    = Restangular.all('countries').getList()
        @scope.theme_list      = Restangular.all('themes').getList()

        # filter method in scope, used by filter form element to launch filter on change
        @scope.filter = @filter
        @scope.getActivatedFilters = @getActivatedFilters
        @scope.removeFilter = @removeFilter
        @scope.removeTheme = @removeTheme
        # when URL change we want that filter updates to
        @scope.$on "$routeUpdate", @onRouteUpdated

    
    getActivatedFilters: ()=>
        return _.where(@scope.filters, {activated: true, stackable:true})

    onRouteUpdated: ()=>
        for f_key, filter of @scope.filters 
            do()=>
                param_value = @routeParams[f_key]
                if filter.type is 'array'
                    if typeof param_value is typeof ""
                        filter.value = param_value.split(',') if param_value?
                    else 
                        filter.value = param_value
                else
                    filter.value = param_value
                    filter.activated = param_value?

    removeTheme: (t)=>
        themes = @scope.filters.themes
        themes.value.splice(themes.value.indexOf(t), 1)

    removeFilter: (filter)=>
        console.log "filter"
        console.log @scope.filters
        filter.activated = false
        filter.value = undefined
        console.log @scope.filters
        @filter()

    addFilter: (params, key, value)=>
        if value? && typeof value == typeof []
            value = value.join(',')
        if value? && value != ""
            params[key] = value
        else
            delete params[key]
        if @scope.filters[key].stackable
            if value?
                @scope.filters[key].activated = true
            else
                @scope.filters[key].activated = false

    filter: =>
        params = @location.search()
        console.log "filter()", @scope , @scope.fitlers 
        @addFilter(params, 'onlySticky',  @scope.filters.onlySticky.value)
        @addFilter(params, 'country',     @scope.filters.country.value)
        @addFilter(params, 'currency',    @scope.filters.currency.value)
        @addFilter(params, 'themes',      @scope.filters.themes.value)
        @location.path("/search/").search(params)

angular.module('stories').controller 'filterCtrl', FilterCtrl