module.exports = (grunt)->
    angular_files = [
        'webapp/static/coffee/*.coffee',  # our scripts 
        'webapp/static/coffee/**/*.coffee',  # our scripts 
        'webapp/templates/*.html', # our templates     
        'webapp/templates/partials/*.html' # our templates     
        'webapp/templates/partials/**/*.html' # our templates     
    ]
    
    packageConfiguration = grunt.file.readJSON('package.json')
    
    getLangISOCodes = ->
        for lang in packageConfiguration.locales.supportedLanguages
            lang.code


    updateSupportedLanguages = ->
        supportedFilePath = packageConfiguration.locales.folder + 'supported.json'
        grunt.file.write(supportedFilePath, JSON.stringify(packageConfiguration.locales.supportedLanguages))


    # Project configuration.
    grunt.initConfig 
           # global application package
        pkg: packageConfiguration
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
    grunt.registerTask 'default', ['available_tasks', 'update_supported_languages']
