# ──────────────────────────────────────────────────────────────────────────────
# The Cards controller handle the cards visualization mode behaviors
# ──────────────────────────────────────────────────────────────────────────────
class CardsCtrl


    @$inject: ['$scope', 'searchService', 'shareService']

    constructor: (@scope, @searchService, Share, @Page) ->
        # ──────────────────────────────────────────────────────────────────────
        # scope variables function binding
        # ──────────────────────────────────────────────────────────────────────
        # Variables
        @scope.onlyRelevantCards = true

        # For sharing purpose
        @scope.currentUrl = Share.getSharingUrl 'cards'

        # Functions
        @scope.search = @searchService
        @scope.showDetails = @showDetails
        @scope.showSharing = @showSharing
        @scope.cardsFilter = @filterCards
        @scope.loadMore = @loadMore

    showDetails: (d)=>
        # show a card detail
        d.show = if d.show is 'infos' then 'preview' else 'infos'

    showSharing: (d)=>
        d.show = if d.show is 'sharing' then 'preview' else 'sharing'

    filterCards: (c)=>
        return false unless c? and _.isObject(c)
        if @scope.onlyRelevantCards
            return c.relevance_score > 6
        return true


    loadMore:()=>
        @scope.onlyRelevantCards = false


angular.module('stories').controller 'cardsCtrl', CardsCtrl