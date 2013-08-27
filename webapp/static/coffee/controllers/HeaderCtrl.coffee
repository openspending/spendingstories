class HeaderCtrl
    @$inject: ['$scope', '$location', 'searchService']

    constructor: (@scope, @location, searchService)->
        # Bi-directional edition of the query
        @scope.query    = _.clone searchService.query
        @scope.currency = _.clone searchService.currency
        
        # Update the header size according the location
        @scope.getHeaderClass = => 
            # If we aren't on the homepage
            # return a class that reduce the header
            if ['/', ''].indexOf( @location.path() ) is -1  then 'reduce'   
        # Submit function to go to the search form
        @scope.search = => 
            if @scope.query?
                # Update path
                @location.path("/search/").search("q", @scope.query).search("c", @scope.currency)

angular.module('stories').controller 'headerCtrl', HeaderCtrl

