class CardsCtrl
    
    @$inject: ['$scope', 'searchService']

    constructor: (@scope, @searchService) ->
        @scope.search = @searchService
        # Select the closest story into the stickies as preview 
        @scope.$watch "this.search.results", @onResultsChanged


    onResultsChanged: =>
        # do stuff 

        
angular.module('stories').controller 'cardsCtrl', CardsCtrl