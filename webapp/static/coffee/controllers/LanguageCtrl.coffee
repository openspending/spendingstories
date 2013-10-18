# LanguageCtrl is responsible of switching languages
class LanguageCtrl
    @$inject: ['$scope','$translate', 'languagesService']
    
    constructor: (@scope, @$translate, @languages)->

        @scope.languages = @languages.supportedLanguages

        @scope.changeLanguage = @changeLanguage

        @scope.$watch =>
            @$translate.uses()
        , (newVal, oldVal)=>
            @scope.language = newVal

        @scope.$watch =>
            # when supportLanguages is loaded from JSON we update scope.languages
                @languages.supportedLanguages
            , =>
                @scope.languages = @languages.supportedLanguages

    changeLanguage: (l)=>
        # called when user click on a language in language list
        @$translate.uses(l.code)


angular.module('stories').controller 'languageCtrl', LanguageCtrl