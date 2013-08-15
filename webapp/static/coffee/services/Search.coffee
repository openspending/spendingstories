angular.module('storiesServices')
    # Create a factory dedicated to research
    .factory("Search", [ 'Restangular', 'Currency', (Restangular, Currency)->
        obj =
            currency : 'USD'
            query    : null
            query_usd: null
            results  : Restangular.all('stories-nested').getList()
            set      : (query, currency='USD')->
                obj.currency = currency
                obj.query    = query
                # USD doesn't need convertion
                if currency is 'USD'
                    obj.query_usd = query    
                else
                    # Performs a USD convertion
                    Currency.get(currency).then (c)->                         
                        obj.query_usd = if c? then query/c.rate else null

                # @TODO Reload the data    
    ])