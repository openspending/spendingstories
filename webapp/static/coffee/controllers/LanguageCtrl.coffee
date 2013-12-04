# LanguageCtrl is responsible of switching languages
class LanguageCtrl
    @$inject: ['$scope','$translate', '$location' ,'languagesService']
    
    constructor: (@scope, @$translate, @location, @languages)->

        @scope.languages      = @languages.supportedLanguages
        @scope.changeLanguage = @changeLanguage
        @init_url_lang        = @location.search()['lang']

        # additional watchings
        @scope.$watch 'current_lang', @currentLangChanged, yes
        @scope.$watch =>
            # when supportLanguages is loaded from JSON we update scope.languages
                @languages.supportedLanguages
            , =>
                @scope.languages = @languages.supportedLanguages
                console.log @languages.supportedLanguages
                if @init_url_lang?
                    @changeLanguage(@init_url_lang)
                    delete @init_url_lang
                else
                    @changeLanguage(@$translate.uses())

        @scope.$watch =>
                @location.search()['lang']
            , (val)=>
                has_changed = (!@scope.current_lang? or val != @scope.current_lang.key)
                if typeof val is 'string' and has_changed
                    @changeLanguage val

    changeLanguage: (lang)=>
        return if !lang?
        if typeof lang is 'string'
            lang = _.findWhere @languages.supportedLanguages, key: lang

        @scope.current_lang = lang
        @languages.current = lang
        @$translate.uses(lang.key)


    currentLangChanged: (lang)=>
        return if !lang?
        # called when user click on a language in language list
        @location.search(
            _.extend @location.search(), lang: lang.key
        )

angular.module('stories').controller 'languageCtrl', LanguageCtrl