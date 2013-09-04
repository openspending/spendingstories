class FilterCtrl
    @$inject: ['$scope', '$routeParams', '$location', 'Currency', 'Restangular']
    constructor: (@scope, @routeParams, @location, Currency, Restangular)->
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

        # filter method in scope, used by filter form element to launch filter on change
        @scope.filter     = @filter
        # when URL change we want that filter updates to
        @scope.$on "$routeUpdate", @onRouteUpdated

    onRouteUpdated: ()=>
        @scope.onlySticky     = @routeParams.onlySticky
        @scope.country        = @routeParams.country
        @scope.currency       = @routeParams.currency
        @scope.selectedThemes = @routeParams.themes

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