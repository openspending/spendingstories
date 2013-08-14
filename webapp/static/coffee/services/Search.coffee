# Services
angular.module('storiesServices', ['ngResource'])
    # Create a factory dedicated to research
    .factory("Search", [ '$resource', '$http', ($resource, $http)->
        query   : null
        results : []
    ])