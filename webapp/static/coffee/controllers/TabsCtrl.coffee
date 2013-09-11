class TabsCtrl

    @$inject: ['$scope', '$location']

    constructor: (@scope, @location) ->
        searchParams = @location.search()
        @MODES =  {
            scale: 'scale'
            cards: 'cards'
        }
        @scope.mode = searchParams.visualization || @MODES.scale 
        @scope.tabs = {
            scale: {
                name: @MODES.scale
                active: @isScaleMode()
            }
            cards: {
                name: @MODES.cards
                active: @isCardsMode()
            }
        }
        # On URL parameters updated we want to update search results
        @scope.$on "$routeUpdate", @onRouteUpdate
        
        @scope.changeVisualization = @changeVisualization

        @scope.isScaleMode = @isScaleMode        
        @scope.isCardsMode  = @isCardsMode

    isCardsMode: ()=>
        @scope.mode == @MODES.cards

    isScaleMode: ()=>
        @scope.mode == @MODES.scale

    changeVisualization: (tab) =>
        @scope.mode = tab.name unless @scope.mode == tab.name
        params = _.extend(@location.search(), {
            visualization: tab.name
        })
        @location.search(params)

    onRouteUpdate: =>
        visualizationMode = @location.search()['visualization']
        tab = @scope.tabs[visualizationMode] if visualizationMode?
        if tab?
            tab.active = true if !tab.active

angular.module('stories').controller 'tabsCtrl', TabsCtrl