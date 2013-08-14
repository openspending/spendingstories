SearchCtrl = ($scope, $routeParams, Search)->
    $scope.search = Search
    # Watch for route change to update the search
    $scope.$watch $routeParams, ->
    	# Update the query property of search according q 
    	$scope.search.query = $routeParams.q if $routeParams.q?


SearchCtrl.$inject = ['$scope', '$routeParams', 'Search'];