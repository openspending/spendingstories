angular.module('storiesServices')
    # Create a factory dedicated to research
    .factory("Search", [ 'Restangular', 'Currency', (Restangular, Currency)->
        obj =
            currency : 'USD'
            query    : null
            query_usd: null
            results  : Restangular.all('stories-nested').getList()
            set      : (query, currency='USD')->                
                # USD doesn't need convertion
                if currency is 'USD'
                    obj.currency  = currency                      
                    obj.query     = query
                    obj.query_usd = query    
                # Performs a USD convertion
                # The currency is already available
                else if Currency.list[currency]?
                    c            = Currency.list[currency]
                    obj.query    = query
                    obj.currency = c.iso_code                    
                    obj.query_usd = if c? then query/c.rate else null
                # The currency isn't loaded yet
                else
                    Currency.get(currency).then (c)->
                        obj.query    = query
                        obj.currency = c.iso_code                    
                        obj.query_usd = if c? then query/c.rate else null

                # @TODO Reload data
    ])