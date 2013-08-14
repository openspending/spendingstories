stories = angular
    .module('stories', ["ui.bootstrap", "restangular", "storiesServices", "storiesFilters"])
    .run(
        [             
            '$rootScope', 
            '$location',
            ($rootScope, $location)->
                # Location available within templates
                $rootScope.location = $location;
        ]
    )
    .config(
        [
            '$interpolateProvider', 
            '$routeProvider', 
            'RestangularProvider',
            ($interpolateProvider, $routeProvider, RestangularProvider)->
                RestangularProvider.setBaseUrl("/api");
                # Avoid a conflict with Django Template's tags
                $interpolateProvider.startSymbol '[['
                $interpolateProvider.endSymbol   ']]'
                # Bind routes to the controllers
                $routeProvider
                    .when('/search/', {
                        controller: SearchCtrl
                        templateUrl: "./partial/search.html",
                    })                    
        ]
    )
