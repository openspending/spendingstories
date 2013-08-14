SearchCtrl = ($scope, $routeParams, Search, Restangular)->
    
    $scope.search = Search
    # Meta value from the server (min, max, etc)
    $scope.meta   = Restangular.all("meta").getList()
    # Watch for route change to update the search
    $scope.$watch $routeParams, ->
        # Update the query property of search according q 
        $scope.search.query = $routeParams.q if $routeParams.q?
        # Update the currency property of search according c
        $scope.search.currency = $routeParams.c if $routeParams.c?

    # Get the filtered result 
    # (no filter yet)
    $scope.userFilter = (d)-> true

    # Only returns the "sticky" stories
    $scope.isTop = (d)-> d.sticky

    # Get the filtered results that are the exact equivalent to the value
    $scope.isEquivalent = (d)-> Math.abs(d.current_value_usd  - $scope.search.query) < 10

SearchCtrl.$inject = ['$scope', '$routeParams', 'Search', 'Restangular'];