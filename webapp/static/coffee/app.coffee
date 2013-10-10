# Declare services once
angular.module('storiesServices', [])


angular
    .module('stories', ["ui.bootstrap", "restangular", "storiesServices", "storiesFilters", "ngCookies"])
    .run(
        [             
            '$rootScope', 
            ($rootScope, $location)->
                # Location available within templates
                $rootScope.location = $location
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
                    .when('/',
                        # Routing without templates: http://stackoverflow.com/a/14412057/885541
                        template: '<!-- leave not empty to avoid useless loading (and bugs) ! -->'
                        controller: 'homeCtrl'
                    )
                    .when('/search/', 
                        controller: 'tabsCtrl'
                        templateUrl: "./partial/search.html"
                        reloadOnSearch: false
                    )
                    .when('/contribute/',
                        controller: 'contributeCtrl'
                        templateUrl: "./partial/contribute.html"
                    )
        ]
    )
