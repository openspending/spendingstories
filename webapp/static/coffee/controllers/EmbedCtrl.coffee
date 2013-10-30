class EmbedCtrl

    @$inject : ['$scope', 'searchService']

    constructor : (@scope, Search) ->
        Search.results.then (data) =>
            if data[0]?
                @scope.d = data[0]
        @scope.showDetails = @showDetails

    showDetails: (d)=>
        # show a card detail
        d.show = if d.show is 'infos' then 'preview' else 'infos'

angular.module 'storiesServices', []
angular.module 'storiesFilters', []
(angular.module 'stories', ['restangular', 'storiesServices', 'storiesFilters', "pascalprecht.translate"])
.run(['$rootScope', ($rootScope)->
    $rootScope.translationLoaded = false
    $rootScope.$on '$translateLoadingSuccess', ()->
        $rootScope.translationLoaded = true
])
.config ['RestangularProvider', '$interpolateProvider', '$translateProvider', (RestangularProvider, $interpolateProvider, $translateProvider) ->
    $translateProvider.useStaticFilesLoader
                prefix: STATIC_URL + 'locales/'
                suffix: '.json'
    $translateProvider.preferredLanguage('en_GB')

    RestangularProvider.setBaseUrl("/api")
    RestangularProvider.setRequestSuffix('/')
    RestangularProvider.setDefaultHttpFields cache: true

    $interpolateProvider.startSymbol '[['
    $interpolateProvider.endSymbol   ']]'
]
(angular.module 'stories').controller 'embedCtrl', EmbedCtrl