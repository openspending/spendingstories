module.exports = (grunt)->
    shell = require('shelljs')
    cmd_opts   = 
        silent: true 
    cmd_result = shell.exec("python scripts/get_supported_languages.py", cmd_opts)
    LANGUAGES = JSON.parse cmd_result.output

    angular_files = [
        'webapp/static/coffee/*.coffee',  # our scripts 
        'webapp/static/coffee/**/*.coffee',  # our scripts 
        'webapp/templates/*.html', # our templates     
        'webapp/templates/partials/*.html' # our templates     
        'webapp/templates/partials/**/*.html' # our templates     
    ]

    # Project configuration.
    grunt.config.init
        # i18n & angular translate configuration 
        i18nextract:
            dev:
                lang: LANGUAGES
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
                tasks: ['makemessages']
        


    # Load the angular translate task
    grunt.loadNpmTasks('grunt-angular-translate')
    grunt.loadNpmTasks('grunt-available-tasks')
    grunt.loadNpmTasks('grunt-contrib-watch')
    grunt.loadNpmTasks('grunt-shell')

    grunt.registerTask 'makemessages', 'i18nextract:dev' 
    grunt.registerTask 'default', ['available_tasks']

    