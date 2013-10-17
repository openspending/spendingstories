class LanguageCtrl
    @$inject: ['$scope','$translate']
    
    constructor: (@scope, @$translate)->
        @scope.languages = [
                name: 'FR'
                code: 'fr_FR'
            ,
                name: 'EN'
                code: 'en_GB'
        ]
        @scope.changeLanguage = @changeLanguage



    changeLanguage: (l)=>
        @scope.language = l.name
        @$translate.uses(l.code)


angular.module('stories').controller 'languageCtrl', LanguageCtrl