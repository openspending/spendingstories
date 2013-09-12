# ──────────────────────────────────────────────────────────────────────────────
# The Cards controller handle the cards visualization mode behaviors 
# ──────────────────────────────────────────────────────────────────────────────
class CardsCtrl
    
    @$inject: ['$scope', 'searchService']

    constructor: (@scope, @searchService) ->
        # ──────────────────────────────────────────────────────────────────────
        # scope function binding  
        # ──────────────────────────────────────────────────────────────────────
        @scope.search = @searchService
        @scope.showDetails = @showDetails
    
    showDetails: (d)=>
        # show a card detail 
        d.details_visible = !d.details_visible

angular.module('stories').controller 'cardsCtrl', CardsCtrl