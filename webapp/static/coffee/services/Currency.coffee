angular.module('storiesServices')
    # Create a factory dedicated to the currency
    .factory("Currency", [ 'Restangular', (Restangular)->
        Restangular.withConfig( (RestangularConfigurer)->
            # This service will be cached
            RestangularConfigurer.setDefaultHttpFields 
                cache: true
            # Transform the response from the server        
            RestangularConfigurer.setResponseExtractor (data)->                                 
                # The array is converted to an object where iso_code i
                _.object _.map(data, (currency)-> [currency.iso_code, currency])                                
        ).all('currencies').getList()
    ])