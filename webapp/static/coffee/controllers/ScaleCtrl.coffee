class ScaleCtrl

    @$inject: ['$scope', 'searchService']

    constructor: (@scope, @searchService) ->
        @scope.search = @searchService
        # Select the closest story into the stickies as preview 
        @scope.$watch "this.search.results", @onResultsChanged
        # Visualization mode
        @scope.overview = false
        # Toggle overview mode
        @scope.toggleOverview = -> @scope.overview = not @scope.overview
        # True if the given value is the equivalent of the query
        @scope.isEquivalent = @isEquivalent
        # Event triggered when we click on a point
        @scope.pointSelection = @setPreviewedStory
        # Select the next story 
        @scope.nextStoryPreview = @nextStoryPreview 
        # Select the previous story 
        @scope.previousStoryPreview = @previousStoryPreview

    # Inherited from VisualizationCtrl
    onResultsChanged: =>
        @scope.search.results.then (data)=>
            # Value to be closed to
            goal = @scope.search.query_usd;
            # Index of the closest value
            closestIdx = 0;
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
        Math.abs(d.current_value_usd  - @scope.search.query_usd) < 10

    nextStoryPreview: ()=>
        @scope.search.results.then (data)=>
            # Get only stories that are in the same group (sticky or not)
            data = _.where data, sticky: @scope.previewedStory.sticky        
            # Sort the data by usd
            data = _.sortBy data, "current_value_usd"
            # Get the current index of the previewed story
            idx  = _.pluck(data, "id").indexOf @scope.previewedStory.id
            # Set the new previewed story
            @scope.previewedStory = data[idx+1] if data[idx+1]?

    previousStoryPreview: ()=>
        @scope.search.results.then (data)=>
            # Get only stories that are in the same group (sticky or not)
            data = _.where data, sticky: @scope.previewedStory.sticky        
            # Sort the data by usd
            data = _.sortBy data, "current_value_usd"
            # Get the current index of the previewed story
            idx  = _.pluck(data, "id").indexOf @scope.previewedStory.id
            # Set the new previewed story
            @scope.previewedStory = data[idx-1] if data[idx-1]?

angular.module('stories').controller 'scaleCtrl', ScaleCtrl