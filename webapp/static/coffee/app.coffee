# Declare services once
angular.module('storiesServices', [])


angular
    .module('stories', ["ui.bootstrap", "restangular", "storiesServices", "storiesFilters", "ngCookies"])
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
            '$httpProvider',
            '$cookiesProvider',
            ($interpolateProvider, $routeProvider, RestangularProvider, $http, $cookies)->
                RestangularProvider.setBaseUrl("/api")
                RestangularProvider.setRequestSuffix('/')
                # All services will be cached
                RestangularProvider.setDefaultHttpFields cache: true   
                # Add csrf token into default post headers
                $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken                
                # Avoid a conflict with Django Template's tags
                $interpolateProvider.startSymbol '[['
                $interpolateProvider.endSymbol   ']]'
                # Bind routes to the controllers
                $routeProvider
                    .when('/search/', 
                        controller: 'searchCtrl'
                        templateUrl: "./partial/search.html"
                        reloadOnSearch: false
                    )
                    .when('/contribute/',
                        controller: ContributeCtrl
                        templateUrl: "./partial/contribute.html"
                    )
        ]
    )
