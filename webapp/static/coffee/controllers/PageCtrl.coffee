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
            _.indexOf(['/', ''], @location.path()) isnt -1

        @scope.setLoading = (loading) =>
            @scope.loading = loading

        Restangular.all('pages').getList(slug:'about').then (data) =>
            if data? and data.length is 1
                @scope.about = data[0].title

        Restangular.all('pages').getList(slug:'faq').then (data) =>
            if data? and data.length is 1
                @scope.faq = data[0].title

angular.module('stories').controller 'pageCtrl', PageCtrl