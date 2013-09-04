
class SearchCtrl
    @$inject: ['$scope', '$location','$routeParams', 'searchService', 'Currency', 'Restangular']

    constructor: (@scope, @location, @routeParams, @searchService, Currency, Restangular) ->
        # Binding of scope variables
        # Visualization mode
        @scope.overview = false
        @scope.search   = @searchService
        @scope.search.set(@location.search())

        # True if search service has some stories
        @scope.hasNormalStories = false
        # True if search service has some sticky stories
        @scope.hasStickyStories = false
        
        # Will set the previous variables based on results 
        @scope.search.results.then @checkStories

        # On URL parameters updated we want to update search results
        @scope.$on "$routeUpdate", @onRouteUpdate
        # Select the closest story into the stickies as preview 
        @scope.$watch "this.search.results", @onSearch

        # Toggle overview mode
        @scope.toggleOverview = -> @scope.overview = not @scope.overview
        # Get the filtered result 
        # (no filter yet)
        @scope.userFilter = (d)-> true
        # True if the given value is the equivalent of the query
        @scope.isEquivalent = @isEquivalent
        # Event triggered when we click on a point
        @scope.pointSelection = @setPreviewedStory
        # Select the next story 
        @scope.nextStoryPreview = @nextStoryPreview 
        # Select the previous story 
        @scope.previousStoryPreview = @previousStoryPreview
    
    onRouteUpdate: =>
        @scope.search.set(@routeParams)
        

    onSearch: =>
        # Value to be closed to
        goal       = @searchService.query_usd;
        # Index of the closest value
        closestIdx = 0;
        # Get all result from search service
        @scope.search.results.then (data)=>
            # Get only stories that are sticky
            data = _.where data, sticky: true

            _.each data, (d, idx)->
                # Current closest value
                closest    = data[closestIdx].current_value_usd
                # Update the closest's idx if needed
                closestIdx = idx if Math.abs(d.current_value_usd - goal) < Math.abs(closest - goal)                
            # Set the value
            @scope.previewedStory = data[closestIdx] if data[closestIdx]?

    setPreviewedStory: (d)=>
        @scope.previewedStory = d

    isEquivalent: (d)=>
        Math.abs(d.current_value_usd  - @search.query_usd) < 10

    nextStoryPreview: ()=>
        # Get all result from search service
        @searchService.results.then (data)=>
            # Get only stories that are in the same group (sticky or not)
            data = _.where data, sticky: @scope.previewedStory.sticky        
            # Sort the data by usd
            data = _.sortBy data, "current_value_usd"
            # Get the current index of the previewed story
            idx  = _.pluck(data, "id").indexOf @scope.previewedStory.id
            # Set the new previewed story
            @scope.previewedStory = data[idx+1] if data[idx+1]?

    previousStoryPreview: ()=>
        # Get all result from search service
        @searchService.results.then (data)=>
            # Get only stories that are in the same group (sticky or not)
            data = _.where data, sticky: @scope.previewedStory.sticky        
            # Sort the data by usd
            data = _.sortBy data, "current_value_usd"
            # Get the current index of the previewed story
            idx  = _.pluck(data, "id").indexOf @scope.previewedStory.id
            # Set the new previewed story
            @scope.previewedStory = data[idx-1] if data[idx-1]?        

angular.module('stories').controller 'searchCtrl', SearchCtrl