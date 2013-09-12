# ──────────────────────────────────────────────────────────────────────────────
# TabsCtrl handle navigation between tabs.
# Each tab is related to a visuzaliton mode (cards or scale)
# ────────────────────────────────────────────────────────────────────────────── 
class TabsCtrl

    @$inject: ['$scope', '$location', 'searchService']

    constructor: (@scope, @location, @searchService) ->
        # ──────────────────────────────────────────────────────────────────────
        # constructor & instance variables
        # ──────────────────────────────────────────────────────────────────────
        searchParams = @location.search()
        @MODES =
            scale: 'scale'
            cards: 'cards'

        # ──────────────────────────────────────────────────────────────────────
        # Scope variables binding // AngularJS Models 
        # ──────────────────────────────────────────────────────────────────────    
        @scope.search = @searchService
        @scope.mode   = searchParams.visualization or @MODES.scale 
        @scope.tabs   = 
            scale: 
                name: @MODES.scale
                active: @isScaleMode()
            cards: 
                name: @MODES.cards
                active: @isCardsMode()

        # ──────────────────────────────────────────────────────────────────────
        # Watchers
        # ──────────────────────────────────────────────────────────────────────
        # On URL parameters updated we want to update search results
        @scope.$on "$routeUpdate", @onRouteUpdate

        # ──────────────────────────────────────────────────────────────────────
        # Scope function binding 
        # ──────────────────────────────────────────────────────────────────────
        @scope.changeVisualization = @changeVisualization
        @scope.isScaleMode = @isScaleMode        
        @scope.isCardsMode = @isCardsMode

    isCardsMode: ()=>
        @scope.mode == @MODES.cards

    isScaleMode: ()=>
        @scope.mode == @MODES.scale

    changeVisualization: (tab) =>
        # change visualization mode & URL params
        @scope.mode = tab.name unless @scope.mode == tab.name
        params = _.extend @location.search(), visualization: tab.name
        @location.search(params)

    onRouteUpdate: =>
        # if URL change we want to update the tab in consequence
        visualizationMode = @location.search()['visualization']
        tab = @scope.tabs[visualizationMode] if visualizationMode?
        tab.active = true if tab? and !tab.active

angular.module('stories').controller 'tabsCtrl', TabsCtrl