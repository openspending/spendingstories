class FilterCtrl
    @$inject: ['$scope', '$routeParams', '$location', 'searchService', 'Currency', 'Restangular']
    constructor: (@scope, @routeParams, @location, @searchService, Currency, Restangular)->
        @searchParams = @location.search()
        @scope.onlySticky     = if @searchParams.onlySticky? then @searchParams.onlySticky
        @scope.country        = if @searchParams.country?    then @searchParams.country
        @scope.currency       = if @searchParams.currency?   then @searchParams.currency
        @scope.selectedThemes = if @searchParams.themes?     then @searchParams.themes.split(',')
        # Not handled for the moment
        # type:       if @searchParams.type?       then @searchParams.type
        @scope.currencies = Currency.list
        @scope.countries  = Restangular.all('countries').getList()
        @scope.themes     = Restangular.all('themes').getList()
        @scope.filter     = @filter

    addFilter: (params, key, value)=>
        if value? && typeof value == typeof []
            value = value.join(',')
        if value? && value != ""
            params[key] = value
        else
            delete params[key]

    filter: =>
        params = @location.search()
        @addFilter(params, 'onlySticky',  @scope.onlySticky)
        @addFilter(params, 'country',     @scope.country)
        @addFilter(params, 'currency',    @scope.currency)
        @addFilter(params, 'themes',      @scope.selectedThemes)
        @location.path("/search/").search(params)

angular.module('stories').controller 'filterCtrl', FilterCtrl