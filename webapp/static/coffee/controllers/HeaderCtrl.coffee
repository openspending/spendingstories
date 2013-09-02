class HeaderCtrl
    @$inject: ['$scope', '$routeParams', '$location', 'searchService', 'Currency', 'Restangular']

    constructor: (@scope, @routeParams, @location, @searchService, Currency, Restangular)->
        @scope.filters = {
            currency: if @routeParams.currency? then @routeParams.currency else undefined
            country:  if @routeParams.country?  then @routeParams.country  else undefined
        }
        # Bi-directional edition of the query
        @scope.$on "$routeUpdate", @onRouteUpdate
        @scope.query    = if @routeParams.q? then @routeParams.q else @searchService.query
        @scope.currency = if @routeParams.c? then @routeParams.c else @searchService.currency
        
        @scope.currencies = Currency.list
        @scope.countries  = Restangular.all('countries').getList()
        @scope.themes     = Restangular.all('themes').getList()
        # Update the header size according the location
        @scope.getHeaderClass = => 
            # If we aren't on the homepage
            # return a class that reduce the header
            if ['/', ''].indexOf( @location.path() ) is -1  then 'reduce'

        # Submit function to go to the search form
        @scope.search = @search
    

    onRouteUpdate: =>
        @scope.query    = @routeParams.q
        @scope.currency = @routeParams.c

        @scope.filters.currency = @routeParams.currency
        @scope.filters.country  = @routeParams.country
        @scope.filters.themes   = @routeParams.themes
        @search()


    search: =>
        if @scope.query?
            params = 
                q: @scope.query
                c: @scope.currency

            filters = {}
            for k, filter of @scope.filters
                do()-> 
                    if filter?
                        filters[k] = filter

            params = _.extend params, filters 

            # Update path
            @location.path("/search/").search(params)
           

angular.module('stories').controller 'headerCtrl', HeaderCtrl

