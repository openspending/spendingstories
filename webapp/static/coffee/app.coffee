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

                RestangularProvider.setBaseUrl("/api")
                RestangularProvider.setRequestSuffix('/')
                # All services will be cached
                RestangularProvider.setDefaultHttpFields cache: true   
                # Add csrf token into default post headers
                $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken                
                # Avoid a conflict with Django Template's tags
                $interpolateProvider.startSymbol '[['
                $interpolateProvider.endSymbol   ']]'

                # Avoid to see translation key
                resolveTranslate = 
                    translationLoaded: ['$rootScope', '$q', ($rootScope, $q)->
                            dfr = $q.defer()
                            unless $rootScope.translationLoaded
                                $rootScope.$on '$translateLoadingSuccess', (data)->
                                    $rootScope.translationLoaded = true
                                    dfr.resolve($rootScope.translationLoaded)
                            else
                                dfr.resolve($rootScope.translationLoaded)
                            return dfr.promise
                        ]

                # Bind routes to the controllers
                $routeProvider
                    .when('/',
                        # Routing without templates: http://stackoverflow.com/a/14412057/885541
                        template: '<!-- leave not empty to avoid useless loading (and bugs) ! -->'
                        controller: 'homeCtrl'
                        reloadOnSearch: false
                        resolve:  resolveTranslate
                    )
                    .when('/search/', 
                        controller: 'tabsCtrl'
                        templateUrl: "./partial/search.html"
                        reloadOnSearch: false
                        resolve:  resolveTranslate
                    )
                    .when('/contribute/',
                        controller: 'contributeCtrl'
                        templateUrl: "./partial/contribute.html"
                        resolve:  resolveTranslate
                    )
                    .when('/about',
                        controller: 'staticPageCtrl'
                        templateUrl: './partial/staticpage.html'
                        resolve:  resolveTranslate
                    )
        ]
    )
