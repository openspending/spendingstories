class StaticPageCtrl

    @$inject : ['$scope', '$location', 'Restangular']

    constructor: (@scope, @location, Restangular) ->
        slug = (do @location.path).substr 1 # Trim the leading /
        # Retrieve the right page through the API
        Restangular.all('pages').getList(slug:slug).then (data) =>
            # If the page exists
            if data.length is 1
                page = data[0]
                # Scope attributes
                @scope.title = page.title
                @scope.content = page.content
                @scope.$parent.setLoading false
            else
                # If the page does not exist, redirect to /
                @location.path '/'

(angular.module 'stories').controller 'staticPageCtrl', StaticPageCtrl