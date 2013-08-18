ContributeCtrl = ($scope, Currency, Restangular)->
    # Start from the first step
    $scope.stepCount  = 3
    $scope.step 	  = 0
    $scope.getForm    = (step=$scope.step)-> $scope["stepForm"+step]
    $scope.loading    = false
    $scope.isDone     = -> $scope.step == $scope.stepCount
    # Currencies list
    $scope.currencies = Currency.list
    # Countries list
    $scope.countries  = Restangular.all("countries").getList()    
    # The story to build
    $scope.story      = currency: 'USD'
    # Send the data to the API
    $scope.submit = ->
        $scope.loading = true
        # Post the story
        Restangular.all("stories").post($scope.story).then -> 
            # Disables loading mode
            $scope.loading = false
            # Then go to last-step + 1 where we thank the contributor
            $scope.step    = $scope.stepCount    
    # Reset the form
    $scope.reset = ->
        $scope.story = currency: 'USD'
        $scope.step  = 0                  



ContributeCtrl.$inject = ['$scope', 'Currency', 'Restangular'];
