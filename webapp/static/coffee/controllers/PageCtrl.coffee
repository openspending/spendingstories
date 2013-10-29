class PageCtrl
    # Injects dependancies    
    @$inject: ['$scope', 'Page', 'Restangular', '$location']

    constructor: (@scope, @Page, Restangular, @location)->
        # ──────────────────────────────────────────────────────────────────────
        # Scope attributes
        # ──────────────────────────────────────────────────────────────────────  
        @scope.Page  = @Page
        @scope.loading = yes

        @scope.getContentClass = =>
            # If we aren't on the homepage
            # return a class that reduce the header
            if _.indexOf(['/', ''], @location.path()) is -1
                no
            else
                yes

        @scope.setLoading = (loading) =>
            @scope.loading = loading

        Restangular.all('pages').getList(slug:'about').then (data) =>
            if data? and data.length is 1
                @scope.about = data[0].title

angular.module('stories').controller 'pageCtrl', PageCtrl