# Declare services once
angular.module('storiesServices', [])


angular
    .module('stories', [
        "ui.bootstrap", "restangular", "storiesServices", "storiesFilters", 
        "ngCookies", "wu.masonry", "pascalprecht.translate"
    ])
    .run(
        [             
            '$rootScope',
            '$location',
            ($rootScope, $location)->
                # Location available within templates
                $rootScope.location = $location
                $rootScope.$on '$translateLoadingSuccess', ()->
                    $rootScope.translationLoaded = true
        ]

    )
    .config(
        [
            '$interpolateProvider', 
            '$routeProvider', 
            '$translateProvider',
            'RestangularProvider',  
            '$httpProvider',
            '$cookiesProvider',
            ($interpolateProvider, $routeProvider, $translateProvider, RestangularProvider, $http, $cookies, $q, $rootScope)->
                $translateProvider.useStaticFilesLoader
                            prefix: STATIC_URL + 'locales/'
                            suffix: '.json'

                $translateProvider.preferredLanguage('en_GB')
                $translateProvider.useMissingTranslationHandlerLog()


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
                    )
                    .when('/search/', 
                        controller: 'tabsCtrl'
                        templateUrl: "./partial/search.html"
                        reloadOnSearch: false
                    )
                    .when('/contribute/',
                        controller: 'contributeCtrl'
                        templateUrl: "./partial/contribute.html"
                        reloadOnSearch: false
                    )
                    .when('/about',
                        controller: 'staticPageCtrl'
                        templateUrl: './partial/staticpage.html'
                    )
        ]
    )
