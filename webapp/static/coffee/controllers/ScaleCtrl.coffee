# ──────────────────────────────────────────────────────────────────────────────
# The Scale controller handles the tabs' behaviors 
# ──────────────────────────────────────────────────────────────────────────────
class ScaleCtrl

    @$inject: ['$scope', 'searchService', 'shareService', 'Restangular']

    constructor: (@scope, @searchService, Share, @Restangular)->
        @scope.search = @searchService
        # Select the closest story into the stickies as preview 
        @scope.search.results.then @onResultsChanged
        @scope.$watch "search.results", @onResultsChanged
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
        @scope.$watch 'previewedStory', @changeTitle

        # For sharing purpose
        @scope.sharingAddress = (d)->
            Share.getSharingAddress d.title
        @scope.embedFrame = (d)->
            Share.getEmbedFrame d.title

        @scope.setLoading no

    changeTitle: => @scope.setTitle @scope.previewedStory.title if @scope.previewedStory?

    onResultsChanged: (results)=>
        @scope.topStories   = _.filter results, (d)-> _.isObject(d) && d.sticky == true
        @scope.otherStories = _.filter results, (d)-> _.isObject(d) && d.sticky == false

        # Set the value
        if @scope.topStories.length
            @scope.previewedStory = @findPreviewedStory(@scope.topStories)
        else if @scope.otherStories.length
            @scope.previewedStory = @findPreviewedStory(@scope.otherStories)
        else
            @scope.previewedStory = undefined


    findPreviewedStory: (stories)=>
        # Index of the closest value
        closestIdx = 0
        # Value to be closed to
        goal = @scope.search.query_usd
        _.each stories, (d, idx)->
            # Current closest value
            closest    = stories[closestIdx].current_value_usd
            # Update the closest's idx if needed
            closestIdx = idx if Math.abs(d.current_value_usd - goal) < Math.abs(closest - goal)   
        
        stories[closestIdx]


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
            idx  = _.indexOf _.pluck(data, "id"), @scope.previewedStory.id
            # Set the new previewed story
            @scope.previewedStory = data[idx+1] if data[idx+1]?

    previousStoryPreview: ()=>
        @scope.search.results.then (data)=>
            # Get only stories that are in the same group (sticky or not)
            data = _.where data, sticky: @scope.previewedStory.sticky        
            # Sort the data by usd
            data = _.sortBy data, "current_value_usd"
            # Get the current index of the previewed story
            idx  = _.indexOf _.pluck(data, "id"), @scope.previewedStory.id
            # Set the new previewed story
            @scope.previewedStory = data[idx-1] if data[idx-1]?

angular.module('stories').controller 'scaleCtrl', ScaleCtrl