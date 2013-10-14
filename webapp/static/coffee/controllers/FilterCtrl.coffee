# ──────────────────────────────────────────────────────────────────────────────
# FilterCtrl handle the filters activated based on URL parameters
# ────────────────────────────────────────────────────────────────────────────── 
class FilterCtrl
    
    @$inject: ['$scope', '$routeParams', '$location', 'Filters', 'Currency', 'Restangular', 'searchService']
    
    constructor: (@scope, @routeParams, @location, @Filters, Currency, Restangular, Search)->
        # ──────────────────────────────────────────────────────────────────────
        # Scope variables bindings                       
        # ──────────────────────────────────────────────────────────────────────
        # Are the filters select lists visible
        @scope.filter_visible = false
        Restangular.all('filters').getList().then (data)=>
            @scope.currency_list = data.currency
            @scope.country_list = data.country
            @scope.theme_list = data.theme

        @scope.search = Search

        @scope.filters = @Filters
        
        # ──────────────────────────────────────────────────────────────────────
        # Scope function bindings                       
        # ──────────────────────────────────────────────────────────────────────
        # filter method in scope, used by filter form element to launch filter on change
        @scope.filter = @filter
        # function to show or hide filter pannel 
        @scope.toggleFilters = @toggleFilters
        # utility function to check if a filter is visible in the current mode 
        @scope.isVisible = @isVisible
        # remove an activated filter 
        @scope.removeFilter = @removeFilter
        # remove an activated theme 
        @scope.removeTheme = @removeTheme
        # reset filters
        @scope.resetFilters = @resetFilters
        @scope.resetComparison = @resetComparison

        @scope.relevanceFilter = @relevanceFilter

        # ──────────────────────────────────────────────────────────────────────
        # Watchers
        # ──────────────────────────────────────────────────────────────────────
        # when URL change we want that filter updates to
        @scope.$on "$routeUpdate", @onRouteUpdated
        # when a filter value change we want to update the URL 
        _.each @scope.filters, (elem, key)=> 
            watch_string = "filters.#{key}.value"
            if elem.type == 'array'
                @scope.$watchCollection watch_string, @filter
            else
                @scope.$watch watch_string, @filter

    relevanceFilter : (story) =>
        return no unless story? and _.isObject(story)
        if story.relevance_score?
            return story.relevance_score > 6
        return yes

    resetFilters : () =>
        for key, filter of @scope.filters
            if key isnt 'title'
                filter.value = undefined

    resetComparison : () =>
        @scope.filters.title.value = undefined

    isVisible:(f)=>
        viz_mode = @location.search().visualization
        _.indexOf(f.modes, viz_mode) != -1

    toggleFilters: =>
        ###
        Produce the closing & the opening of the filters bar
        ### 
        @scope.filter_visible = !@scope.filter_visible

    onRouteUpdated: ()=>
        ###
        On URL changes we want to retrieve the URL params of filters and bind 
        them with our @scope.filters model 
        ### 
        viz_mode = @location.search().visualization
        for f_key, filter of @scope.filters            
            if _.indexOf(filter.modes, viz_mode) == -1
                # if URL has a filter disabled in one mode we have to delete
                # it from URL.
                @removeFilter(filter)
            else 
                param_value = @routeParams[f_key]
                if filter.type is 'array'
                    if typeof param_value is typeof ""
                        filter.value = param_value.split(',') if param_value?
                    else 
                        filter.value = param_value
                else
                    filter.value = param_value
                    filter.activated = param_value?

    removeTheme: (index)=>
        # Called if user click on a theme to delete it (in activated filters bar)
        themes = @scope.filters.themes
        themes.value.splice(index, 1)

    removeFilter: (filter)=>
        # Called when a user click to remove a filter in activated filters bar
        filter.value = undefined

    addFilter: (params, key, value)=>
        ### 
        Add a filter to the URL params and delete it if its value is undefined 
        Will check passed value type and process it to set a proper value in URL
        ### 
        if value? && typeof value == typeof []
            value = value.join(',')
        if value? && value != ""
            params[key] = value
        else
            delete params[key]
        if @scope.filters[key].stackable
            @scope.filters[key].activated = value?

    filter: ()=>
        ### 
        Called when filter changes, we retrieve all filter and change the URL in
        consequence
        ###
        params = @location.search()
        @addFilter(params, key, filter.value) for key, filter of @scope.filters
        @location.search(params)

angular.module('stories').controller 'filterCtrl', FilterCtrl