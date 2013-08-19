SearchCtrl = ($scope, $routeParams, Search)->
    
    $scope.search     = Search
    # Visualization mode
    $scope.overview   = false
    # Watch for route change to update the search
    $scope.$watch $routeParams, ->readRouteParams()
    # Watch for search change to update the search
    $scope.$on "$routeUpdate", ->readRouteParams()

    # Select the closest story into the stickies as preview    
    $scope.$watch "search", ->        
        # Value to be closed to
        goal       = Search.query_usd;
        # Index of the closest value
        closestIdx = 0;
        # Get all result from Search service
        Search.results.then (data)->            
            # Get only stories that are sticky
            data = _.where data, sticky: true

            _.each data, (d, idx)->
                # Current closest value
                closest    = data[closestIdx].current_value_usd
                # Update the closest's idx if needed
                closestIdx = idx if Math.abs(d.current_value_usd - goal) < Math.abs(closest - goal)                
            # Set the value
            $scope.previewedStory = data[closestIdx] if data[closestIdx]?
    
    # Read the route params to update search
    readRouteParams = ->  
        # Update the query property of search according q 
        $scope.search.set($routeParams.q, $routeParams.c) if $routeParams.q?

    # Toggle overview mode
    $scope.toggleOverview = -> $scope.overview = not $scope.overview
    # Get the filtered result 
    # (no filter yet)
    $scope.userFilter = (d)-> true
    # True if the given value is the equivalent of the query
    $scope.isEquivalent = (d)-> Math.abs(d.current_value_usd  - $scope.search.query_usd) < 10
    
    # Event triggered when we click on a point
    $scope.pointSelection = (d)-> $scope.previewedStory = d
    # Select the next story 
    $scope.nextStoryPreview = ()->
        # Get all result from Search service
        Search.results.then (data)->
            # Get only stories that are in the same group (sticky or not)
            data = _.where data, sticky: $scope.previewedStory.sticky        
            # Sort the data by usd
            data = _.sortBy data, "current_value_usd"
            # Get the current index of the previewed story
            idx  = _.pluck(data, "id").indexOf $scope.previewedStory.id
            # Set the new previewed story
            $scope.previewedStory = data[idx+1] if data[idx+1]?
    # Select the previous story 
    $scope.previousStoryPreview = ()->
        # Get all result from Search service
        Search.results.then (data)->
            # Get only stories that are in the same group (sticky or not)
            data = _.where data, sticky: $scope.previewedStory.sticky        
            # Sort the data by usd
            data = _.sortBy data, "current_value_usd"
            # Get the current index of the previewed story
            idx  = _.pluck(data, "id").indexOf $scope.previewedStory.id
            # Set the new previewed story
            $scope.previewedStory = data[idx-1] if data[idx-1]?        


SearchCtrl.$inject = ['$scope', '$routeParams', 'Search'];