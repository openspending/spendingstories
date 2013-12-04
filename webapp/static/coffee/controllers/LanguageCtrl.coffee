# LanguageCtrl is responsible of switching languages
class LanguageCtrl
    @$inject: ['$scope', '$location' ,'languagesService']
    
    constructor: (@scope, @location, @languages)->

        @scope.languages      = @languages
        @scope.changeLanguage = @changeLanguage
        @init_url_lang        = @location.search()['lang']

        # additional watchings
        @scope.$watch 'languages.current', @currentLangChanged, yes
        @scope.$watch =>
            # when supportLanguages is loaded from JSON we update scope.languages
                @languages.list
            , =>
                if @init_url_lang?
                    @changeLanguage(@init_url_lang)
                    delete @init_url_lang
                else
                    @changeLanguage()

        @scope.$watch =>
                @location.search()['lang']
            , (val)=>
                has_changed = val != @languages.current
                if typeof val is 'string' and has_changed
                    @changeLanguage val

    changeLanguage: (lang)=>
        return if !lang?
        @languages.setCurrent lang 

    currentLangChanged: (lang)=>
        return if !lang?
        # called when user click on a language in language list
        @location.search(
            _.extend @location.search(), lang: @languages.current
        )

angular.module('stories').controller 'languageCtrl', LanguageCtrl