ContributeCtrl = ($scope, Currency, Restangular)->
    # Start from the first step
    $scope.step = 2
    # Currencies list
    $scope.currencies = Currency.list
    # Countries list
    $scope.countries  = Restangular.all("countries").getList()
    # Forms default value
    $scope.currency = 'USD'
    $scope.amount   = 1111
    $scope.title    = "Royal weeding"
    $scope.year     = 2012
    $scope.country  = "FRA"


ContributeCtrl.$inject = ['$scope', 'Currency', 'Restangular'];
