class HeaderCtrl
    @$inject: [
        # AngularJS + vendor dependencies injection
        '$scope', '$routeParams', '$location','$filter', '$translate'
        # Custom services injection 
        'comprehensionService', 'Currency', 'humanizeService', 'Page']

    constructor: (@scope,@routeParams,@location,@filter,@$translate,@Comprehension,@Currency,@Humanize, @Page)->
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
            if !@isOnHome()
                'reduce'
            else
                @scope.user_query = undefined
                key = 'HEADER_SEARCH_PLACEHOLDER'
                title = $translate(key)
                if title isnt key
                    @Page.setTitle title


        # Submit function to go to the search form
        @scope.search = @onSearch
        @scope.propositions = @getPropositions

        # little trick to force digest on typeahead
        @scope.$watch ()=>
                @Currency.loaded
            , (val)=>
                @scope.currenciesLoaded = val

        @scope.$watch ()=>
                @$translate.uses()
            ,  (val)=>
                @scope.language = val

        @scope.clicked = no

    isOnHome: =>
        !(_.indexOf(['/', ''], @location.path()) is -1)

    onSearch: =>
        params = {}

        # Get the first suggestion as our query when the Compare button is clicked
        if @scope.compareclick
            if @scope.searchform.query.$viewValue?
                query = _.first (@getPropositions @scope.searchform.query.$viewValue)
                @scope.user_query = query
                @scope.searchform.query.$setViewValue do =>
                    (@filter 'humanizeValue') query.number, query.currency
                do @scope.searchform.query.$render

        if @scope.user_query? or @scope.compareclick
            params = _.extend @location.search(), {
                q: @scope.user_query.number
                c: @scope.user_query.currency
            }

        if _.indexOf(@location.path(), 'search') == -1
            @location.path('/search/').search(params)
        else
            # Update path
            @location.search(params)

        @scope.compareclick = no

    getPropositions: (viewValue) =>
            @Comprehension.getPropositions viewValue


angular.module('stories').controller 'headerCtrl', HeaderCtrl

