# Services
angular.module('storiesServices', [])
    # Create a factory dedicated to research
    .factory("Search", [ 'Restangular', (Restangular)->
        query   : null
        currency: 'dollars'
        results : Restangular.all('stories').getList()
    ])