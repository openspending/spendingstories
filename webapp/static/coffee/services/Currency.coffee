angular.module('storiesServices')
    # Create a factory dedicated to the currency
    .factory("Currency", [ 'Restangular', (Restangular)->
        obj = 
            loaded: false
            all : Restangular.all('currencies')
            get : (iso_code) -> obj.all.one(iso_code).get()
            list: {}

        # Load data once for syncrhone query
        obj.all.getList().then (data)->
            # Some objects aren't a currency object                   
            data = _.filter data, (currency)-> currency and currency.iso_code? 
            # The array is converted to an object where iso_code i
            data = _.object _.map(data, (currency)-> [currency.iso_code, currency])                                    
            # Extend the parent object to keep the same object reference
            obj.list = _.extend obj.list, data
            obj.loaded = true

        return obj
    ])