# HomeCtrl is used to set title when / route is reached 
class HomeCtrl
    @$inject: ['$translate', 'Page']

    constructor: ($translate, @Page)->
        @Page.setTitle($translate('HEADER_SEARCH_PLACEHOLDER'))

angular.module('stories').controller 'homeCtrl', HomeCtrl
