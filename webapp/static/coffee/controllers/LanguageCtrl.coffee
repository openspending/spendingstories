# LanguageCtrl is responsible of switching languages
class LanguageCtrl
    @$inject: ['$scope', '$location' ,'languagesService']
    
    constructor: (@scope, @location, @languages)->

        @scope.languages = @languages
        @changeLanguage @location.search()['lang'] 

        # additional watchings
        @scope.$watch 'languages.current', @currentLangChanged
        @scope.$watch =>
                @location.search()['lang']
            , (val)=>
                has_changed = val != @languages.current
                if typeof val is 'string' and has_changed
                    @changeLanguage val

    changeLanguage: (lang)=>
        @scope.languages.setCurrent lang

    currentLangChanged: (lang)=>
        return if !lang?
        # called when user click on a language in language list
        @location.search(
            _.extend @location.search(), lang: @languages.current
        )

angular.module('stories').controller 'languageCtrl', LanguageCtrl