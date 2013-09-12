class CardsCtrl
    
    @$inject: ['$scope', 'searchService']

    constructor: (@scope, @searchService) ->
        @scope.search = @searchService
        @scope.showDetails = @showDetails
    
    showDetails: (d)=>
        d.details_visible = !d.details_visible


        
angular.module('stories').controller 'cardsCtrl', CardsCtrl