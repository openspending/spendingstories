class HeaderCtrl
    @$inject: ['$scope', '$routeParams', '$location', 'comprehensionService']

    constructor: (@scope, @routeParams, @location, @comprehension)->
        @searchParams   = @location.search()
        @scope.query    = if @searchParams.q? then parseInt(@searchParams.q)
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
        if @scope.query?
            params = _.extend @location.search(), {
                q: @scope.query
                c: @scope.currency
            }
        if @location.path().indexOf('search') == -1
            @location.path('/search/').search(params)
        else
            # Update path
            @location.search(params)

    getPropositions: =>
            @comprehension.getPropositions @scope.query


angular.module('stories').controller 'headerCtrl', HeaderCtrl

