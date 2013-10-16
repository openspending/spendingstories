module.exports = (grunt)->
    angular_files = [
        'webapp/static/coffee/*.coffee',  # our scripts 
        'webapp/static/coffee/**/*.coffee',  # our scripts 
        'webapp/templates/*.html', # our templates     
        'webapp/templates/partials/*.html' # our templates     
        'webapp/templates/partials/**/*.html' # our templates     
    ]
    # Project configuration.
    grunt.initConfig 
        # global application package
        pkg: grunt.file.readJSON('package.json')
        # i18n & angular translate configuration 
        i18nextract:
            dev:
                lang: ['en_GB', 'fr_FR'],
                src: angular_files,
                suffix: ".json"
                dest: "webapp/static/locales"
        # auto generate i18n json files 
        watch:
            i18n:
                files: angular_files
                tasks: ['i18nextract:dev']

    # Load the angular translate task
    grunt.loadNpmTasks('grunt-contrib-watch')
    grunt.loadNpmTasks('grunt-angular-translate')

    grunt.registerTask 'default', ['watch']