class PageCtrl
    # Injects dependancies    
    @$inject: ['$scope', 'Page', 'Restangular']

    constructor: (@scope, @Page, Restangular)->
        # ──────────────────────────────────────────────────────────────────────
        # Scope attributes
        # ──────────────────────────────────────────────────────────────────────  
        @scope.Page  = @Page

        Restangular.all('pages').getList(slug:'about').then (data) =>
            if data? and data.length is 1
                @scope.about = data[0].title

angular.module('stories').controller 'pageCtrl', PageCtrl