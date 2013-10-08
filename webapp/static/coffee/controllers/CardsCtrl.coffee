# ──────────────────────────────────────────────────────────────────────────────
# The Cards controller handle the cards visualization mode behaviors 
# ──────────────────────────────────────────────────────────────────────────────
class CardsCtrl
    
    @$inject: ['$scope', 'searchService']

    constructor: (@scope, @searchService, @Page) ->
        @onlyRelevantCards = true 
        # ──────────────────────────────────────────────────────────────────────
        # scope function binding  
        # ──────────────────────────────────────────────────────────────────────
        @scope.search = @searchService
        @scope.showDetails = @showDetails
        @scope.cardsFilter = @filterCards
        @scope.loadMore = @loadMore

    showDetails: (d)=>
        # show a card detail 
        d.details_visible = !d.details_visible

    filterCards: (c)=>
        if @onlyRelevantCards
            return c.relevance_score > 6
        return true

    loadMore:()=>
        @onlyRelevantCards = false


angular.module('stories').controller 'cardsCtrl', CardsCtrl