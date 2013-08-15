SearchCtrl = ($scope, $routeParams, Search, Currency)->
    
    $scope.search     = Search
    $scope.currencies = Currency
    # Watch for route change to update the search
    $scope.$watch $routeParams, ->
        # Update the query property of search according q 
        $scope.search.set($routeParams.q, $routeParams.c)  if $routeParams.q?

    # Get the filtered result 
    # (no filter yet)
    $scope.userFilter = (d)-> true

    # Get the filtered results that are the exact equivalent to the value
    $scope.isEquivalent = (d)-> Math.abs(d.current_value_usd  - $scope.search.query) < 10
    # Showed equivalent
    $scope.equivalentIdx = 0

SearchCtrl.$inject = ['$scope', '$routeParams', 'Search', 'Currency'];