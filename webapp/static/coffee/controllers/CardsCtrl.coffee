# ──────────────────────────────────────────────────────────────────────────────
# The Cards controller handle the cards visualization mode behaviors 
# ──────────────────────────────────────────────────────────────────────────────
class CardsCtrl
    
    @$inject: ['$scope', 'searchService']

    constructor: (@scope, @searchService, @Page) ->

        # ──────────────────────────────────────────────────────────────────────
        # scope variables function binding  
        # ──────────────────────────────────────────────────────────────────────
        # Variables
        @scope.onlyRelevantCards = true 
        # Functions
        @scope.search = @searchService
        @scope.showDetails = @showDetails
        @scope.cardsFilter = @filterCards
        @scope.loadMore = @loadMore

    showDetails: (d)=>
        # show a card detail 
        d.details_visible = !d.details_visible

    filterCards: (c)=>
        return false unless c? and _.isObject(c)
        if @scope.onlyRelevantCards
            return c.relevance_score > 6
        return true


    loadMore:()=>
        @scope.onlyRelevantCards = false


angular.module('stories').controller 'cardsCtrl', CardsCtrl