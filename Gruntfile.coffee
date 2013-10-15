module.exports = (grunt)->
  # Project configuration.
  grunt.initConfig 
    # global application package
    pkg: grunt.file.readJSON('package.json')
    # i18n & angular translate configuration 
    i18nextract:
        dev: 
            lang: ['en_GB', 'fr_FR'],
            src: [
                'webapp/coffee/**',  # our scripts 
                'webapp/coffee/**/*.coffee',  # our scripts 
                'webapp/templates/*.html', # our templates     
                'webapp/templates/partials/*.html' # our templates     
                'webapp/templates/partials/**/*.html' # our templates     
            ],
            suffix: ".json"
            dest: "webapp/static/locales"

  # Load the angular translate task
  grunt.loadNpmTasks('grunt-angular-translate')

  grunt.registerTask 'makemessages', ['i18nextract:dev']
  grunt.registerTask 'default', ['makemessages']