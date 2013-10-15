class StaticPageCtrl

    @$inject : ['$scope', '$location', 'Restangular']

    constructor: (@scope, @location, Restangular) ->
        slug = (do @location.path).substr 1 # Trim the leading /
        Restangular.all('pages').getList(slug:slug).then (data) =>
            if data.length is 1
                @scope.content = data[0].content

(angular.module 'stories').controller 'staticPageCtrl', StaticPageCtrl