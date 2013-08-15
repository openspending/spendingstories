angular.module('storiesServices')
    # Create a factory dedicated to the currency
    .factory("Meta", [ 'Restangular', (Restangular)->
        Restangular.withConfig( (RestangularConfigurer)->
            # This service will be cached
            RestangularConfigurer.setDefaultHttpFields cache: true
        ).all('meta').getList()
    ])