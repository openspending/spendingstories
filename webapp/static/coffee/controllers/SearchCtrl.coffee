SearchCtrl = ($scope, $routeParams, Search, Currency)->
    
    $scope.search     = Search
    $scope.currencies = Currency
    # Watch for route change to update the search
    $scope.$watch $routeParams, ->
        # Update the query property of search according q 
        $scope.search.set($routeParams.q, $routeParams.c) if $routeParams.q?

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
        # Select the next story 
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

    $scope.previewedStory = 
        id: 84
        sticky: true


SearchCtrl.$inject = ['$scope', '$routeParams', 'Search', 'Currency'];