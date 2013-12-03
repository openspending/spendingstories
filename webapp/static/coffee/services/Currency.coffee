angular.module('storiesServices')
    # Create a factory dedicated to the currency
    .factory("Currency", [ 'Restangular', (Restangular)->
        obj = 
            loaded: false
            all : Restangular.all('currencies')
            get : (iso_code) ->
                _.find obj.list, (c) -> iso_code == c.iso_code
            list: []

        # Load data once for syncrhone query
        obj.all.getList().then (data)->
            # Some objects aren't a currency object                   
            data       = _.filter data, (currency)-> currency and currency.iso_code?
            obj.list   = data
            obj.loaded = true

        return obj
    ])
