module.exports = (grunt)->
    
    locales = {
        folder: "webapp/static/locales/",
        supportedLanguages: [
                name: "French",
                code: "fr_FR"
            , 
                name: "English",
                code: "en_GB"
        ]
    }

    angular_files = [
        'webapp/static/coffee/*.coffee',  # our scripts 
        'webapp/static/coffee/**/*.coffee',  # our scripts 
        'webapp/templates/*.html', # our templates     
        'webapp/templates/partials/*.html' # our templates     
        'webapp/templates/partials/**/*.html' # our templates     
    ]
    
    getLangISOCodes = ->
        for lang in locales.supportedLanguages
            lang.code


    updateSupportedLanguages = ->
        supportedFilePath = locales.folder + 'supported.json'
        grunt.file.write(supportedFilePath, JSON.stringify(locales.supportedLanguages))
        grunt.log.writeln("File 'supported.json' updated in #{locales.folder} folder")


    # Project configuration.
    grunt.initConfig 
           # global application package
        # i18n & angular translate configuration 
        i18nextract:
            dev:
                lang: getLangISOCodes()
                src: angular_files
                suffix: ".json"
                dest: "webapp/static/locales"
                interpolation: 
                    startSymbol: '[['
                    endSymbol: ']]'
        # auto generate i18n json files 
        watch:
            i18n:
                files: angular_files
                tasks: ['i18nextract:dev']
        

    # Load the angular translate task
    grunt.loadNpmTasks('grunt-contrib-watch')
    grunt.loadNpmTasks('grunt-available-tasks')
    grunt.loadNpmTasks('grunt-angular-translate')

    grunt.registerTask 'update_supported_languages',
        'Update or create the supported.json files in the locales folder', 
        updateSupportedLanguages

    grunt.registerTask 'makemessages', ['i18nextract:dev']
    grunt.registerTask 'default', ['available_tasks']
