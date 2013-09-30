class HeaderCtrl
    @$inject: ['$scope', '$routeParams', '$location', 'comprehensionService']

    constructor: (@scope, @routeParams, @location, @comprehension)->
        @searchParams   = @location.search()
        @scope.user_query = undefined
        
        @scope.query = if @searchParams.q? then parseInt(@searchParams.q) else null
        
        @scope.currency = if @searchParams.c? then @searchParams.c else 'USD'

        # Update the header size according the location
        @scope.getHeaderClass = =>
            # If we aren't on the homepage
            # return a class that reduce the header
            if ['/', ''].indexOf( @location.path() ) is -1  then 'reduce'

        # Submit function to go to the search form
        @scope.search = @onSearch
        @scope.propositions = @getPropositions

    onSearch: =>
        params = {}
        console.log @scope.user_query
        if @scope.user_query?
            params = _.extend @location.search(), {
                q: @scope.user_query.number
                c: @scope.user_query.currency
            }
        if @location.path().indexOf('search') == -1
            @location.path('/search/').search(params)
        else
            # Update path
            @location.search(params)

    getPropositions: =>
            @comprehension.getPropositions @scope.user_query


angular.module('stories').controller 'headerCtrl', HeaderCtrl

