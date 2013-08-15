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

    $scope.pointSelection = (d)-> 
        $scope.preview.id = d.id
    # Showed equivalent
    $scope.preview = id: 84

SearchCtrl.$inject = ['$scope', '$routeParams', 'Search', 'Currency'];