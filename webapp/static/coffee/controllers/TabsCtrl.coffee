# ──────────────────────────────────────────────────────────────────────────────
# TabsCtrl handle navigation between tabs.
# Each tab is related to a visuzaliton mode (cards or scale)
# ────────────────────────────────────────────────────────────────────────────── 
class TabsCtrl

    @$inject: ['$scope', '$location', 'searchService', 'Page', 'Filters']

    constructor: (@scope, @location, @searchService, @Page, @Filters) ->
        # ──────────────────────────────────────────────────────────────────────
        # constructor & instance variables
        # ──────────────────────────────────────────────────────────────────────
        searchParams = @location.search()
        # Activate filters for this view
        @Page.hasFilters = true
        # Remove filter mode when leaving the controller
        @scope.$on "$destroy", => @Page.hasFilters = false
        # Available modes 
        @scope.MODES = @MODES = 
            scale: 'scale'
            cards: 'cards'
        # ──────────────────────────────────────────────────────────────────────
        # Scope variables binding // AngularJS Models 
        # ──────────────────────────────────────────────────────────────────────    
        @scope.search  = @searchService
        @scope.filters = @Filters
        @scope.mode    = searchParams.visualization or @MODES.scale 
        @scope.tabs    = 
            scale: 
                name: @MODES.scale
                active: @isScaleMode()
                title: undefined
            cards: 
                name: @MODES.cards
                active: @isCardsMode()
                title: undefined
        # ──────────────────────────────────────────────────────────────────────
        # Watchers
        # ──────────────────────────────────────────────────────────────────────
        # On URL parameters updated we want to update search results
        @scope.$on "$routeUpdate", @onRouteUpdate
        # On mode changes we want to get the appropriated title
        @scope.$watch 'mode', @onModeChanged

        # ──────────────────────────────────────────────────────────────────────
        # Scope function binding 
        # ──────────────────────────────────────────────────────────────────────
        @scope.changeVisualization = @changeVisualization
        @scope.isScaleMode         = @isScaleMode        
        @scope.isCardsMode         = @isCardsMode
        @scope.setTitle            = @setTitle
        @scope.hasActivatedFilters = @hasActivatedFilters
        @scope.getActivatedFilters = @getActivatedFilters 
        @scope.removeFilter        = @removeFilter
        @scope.removeTheme         = @removeTheme

    setTitle: (tab, title)=>
        @scope.tabs[tab].title = title 
        @updateTitle()


    updateTitle: =>
        title =  @scope.mode
        subtitle = @scope.tabs[@scope.mode].title
        if subtitle?
            title = "#{title} / #{subtitle}"
        @Page.setTitle title

    isCardsMode: ()=>
        @scope.mode == @MODES.cards

    isScaleMode: ()=>
        @scope.mode == @MODES.scale
    
    removeTheme: (index)=>
        # Called if user click on a theme to delete it (in activated filters bar)
        themes = @scope.filters.themes
        themes.value.splice(index, 1)

    removeFilter: (filter)=>
        # Called when a user click to remove a filter in activated filters bar
        filter.value = undefined

    hasActivatedFilters: ()=>
        themes = @Filters.themes.value
        @getActivatedFilters().length || (themes != undefined && themes.length > 0)

    getActivatedFilters: ()=>
        # Returns filters that have been activated (i.e: filters set by the user)
        _.filter(@Filters, (f)-> f.value? && f.stackable)

    onModeChanged: ()=>
        title = angular.element($('.active')).scope().title 

    changeVisualization: (tab) =>
        # change visualization mode & URL params
        @scope.mode = tab.name unless @scope.mode == tab.name
        params = _.extend @location.search(), visualization: tab.name
        @location.search(params)

    onRouteUpdate: =>
        query = (do @location.search).q
        if not query? or query is ''
            @location.path '/'
        # if URL change we want to update the tab in consequence
        visualizationMode = @location.search()['visualization']
        tab = @scope.tabs[visualizationMode] if visualizationMode?
        tab.active = true if tab? and !tab.active

angular.module('stories').controller 'tabsCtrl', TabsCtrl