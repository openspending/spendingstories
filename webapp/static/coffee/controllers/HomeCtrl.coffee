# HomeCtrl is used to set title when / route is reached 
class HomeCtrl
    @$inject: ['Page']

    constructor: (@Page)-> @Page.setTitle('How much is it really')

angular.module('stories').controller 'homeCtrl', HomeCtrl
