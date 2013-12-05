'''
Overrides the django `makemessages` command to collect also i18n strings with 
a grunt task also called "makemessages" 

For more information about the grunt task check the Gruntfile.coffee at the 
project root
'''
from django.core.management.commands.makemessages \
    import Command as BaseMakeMessages
from optparse \
    import make_option
import os

def grunt(cmd): 
    os.system('grunt %s'  % cmd)

class Command(BaseMakeMessages):
    option_list = BaseMakeMessages.option_list + (
        make_option('--static-only', default=False, dest='static_only', 
            help='Extract only the static locales (for angular application)',
            action='store_true'),
    )

    help = ("Will extract the i18n strings from the project and write them into"
            "conf/locale for .po files (extracted by django makemessages base " 
            "command) and in webapp/static/locales/ for static app translation")

    def handle_noargs(self, *args, **options):
        static_only = options.get('static_only')
        grunt('makemessages')
        if not static_only:
            super(Command, self).handle_noargs(*args, **options)

