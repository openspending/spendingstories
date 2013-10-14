class HeaderCtrl
    @$inject: ['$scope', '$routeParams', '$location','$filter','comprehensionService', 'Currency']

    constructor: (@scope, @routeParams, @location,@filter, @comprehension, @Currency)->
        @searchParams = @location.search()
        @scope.currenciesLoaded = @Currency.loaded
        @scope.user_query = undefined
        if @searchParams.q?
            @scope.user_query = 
                number: parseInt(@searchParams.q)
                currency: @searchParams.c 

        # Update the header size according the location
        @scope.getHeaderClass = =>
            # If we aren't on the homepage
            # return a class that reduce the header
            if _.indexOf(['/', ''], @location.path()) is -1  then 'reduce'

        # Submit function to go to the search form
        @scope.search = @onSearch
        @scope.propositions = @getPropositions

        # little trick to force digest on typeahead
        @scope.$watch ()=>
                @Currency.loaded
            , (val)=>
                @scope.currenciesLoaded = val

    onSearch: =>
        params = {}
        if @scope.user_query?
            params = _.extend @location.search(), {
                q: @scope.user_query.number
                c: @scope.user_query.currency
            }
        if _.indexOf(@location.path(), 'search') == -1
            @location.path('/search/').search(params)
        else
            # Update path
            @location.search(params)

    getPropositions: (viewValue) =>
            @comprehension.getPropositions viewValue


angular.module('stories').controller 'headerCtrl', HeaderCtrl

