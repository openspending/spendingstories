# ──────────────────────────────────────────────────────────────────────────────
# FilterCtrl handle the filters activated based on URL parameters
# ────────────────────────────────────────────────────────────────────────────── 
class FilterCtrl
    
    @$inject: ['$scope', '$routeParams', '$location', 'Currency', 'Restangular']
    
    constructor: (@scope, @routeParams, @location, Currency, Restangular)->
        @searchParams = @location.search()
        # ──────────────────────────────────────────────────────────────────────
        # Scope variables bindings                       
        # ──────────────────────────────────────────────────────────────────────
        # Are the filters select lists visible
        @scope.filter_visible = false
        # filter list values 
        @scope.currency_list = Restangular.all('filters/currencies').getList isUsed:true
        @scope.country_list  = Restangular.all('filters/countries').getList isUsed:true
        @scope.theme_list    = Restangular.all('filters/themes').getList isUsed:true
        # filters models 
        @scope.filters = 
            ### 
            Each filter can be described as following :
                @stackable:
                    the filter can be added to the "filter bar"
                @type:      
                    the type of the filter value
                @value:     
                    the current filter value 
                @modes:
                    array of supported visualization mode for the filter 
                    will hide the filter if it's not supported and remove 
                    this parameters from url.
            ### 
            onlySticky:
                stackable: false
                type: 'boolean'
                value: @searchParams.onlySticky
                modes: ['cards']
            country:
                name: 'Country'
                type: 'string'
                stackable: true 
                value: @searchParams.country
                modes: ['cards', 'scale']
            currency:
                name: 'Currency'
                type: 'string'
                stackable: true
                value: @searchParams.currency
                modes: ['cards', 'scale']
            themes:
                type: 'array'
                stackable: false
                value: if @searchParams.themes? then @searchParams.themes.split(',')
                modes: ['cards', 'scale']
            # Not handled for the moment
            # type:
                # name: 'Type'
                # type: 'string'
                # stackable: true 
                # value: if @searchParams.type? then @searchParams.type
                # modes: ['cards', 'scale']

        # ──────────────────────────────────────────────────────────────────────
        # Scope function bindings                       
        # ──────────────────────────────────────────────────────────────────────
        # filter method in scope, used by filter form element to launch filter on change
        @scope.filter = @filter
        # function to show or hide filter pannel 
        @scope.toggleFilters = @toggleFilters
        @scope.hasActivatedFilters = @hasActivatedFilters
        @scope.getActivatedFilters = @getActivatedFilters
        # utility function to check if a filter is visible in the current mode 
        @scope.isVisible = @isVisible
        # remove an activated filter 
        @scope.removeFilter = @removeFilter
        # remove an activated theme 
        @scope.removeTheme = @removeTheme

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

    isVisible:(f)=>
        viz_mode = @location.search().visualization
        _.indexOf(f.modes, viz_mode) != -1

    toggleFilters: =>
        ###
        Produce the closing & the opening of the filters bar
        ### 
        @scope.filter_visible = !@scope.filter_visible

    hasActivatedFilters: ()=>
        themes = @scope.filters.themes.value
        @getActivatedFilters().length || (themes != undefined && themes.length > 0)

    getActivatedFilters: ()=>
        # Returns filters that have been activated (i.e: filters set by the user)
        _.filter(@scope.filters, (f)-> f.value? && f.stackable)

    onRouteUpdated: ()=>
        ###
        On URL changes we want to retrieve the URL params of filters and bind 
        them with our @scope.filters model 
        ### 
        viz_mode = @location.search().visualization
        for f_key, filter of @scope.filters
            do()=>
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