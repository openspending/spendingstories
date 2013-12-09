'''
Little command to download and process translation from crowdin translation 
platform
'''
from optparse import make_option
from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from django.core.management import call_command
import os


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--update-only', default=False, dest='update_only', 
            help='Will download the locales from crowdin platform without compiling the result',
            action='store_true'),
    )

    def handle_noargs(self,  *args, **options):
        self.check_install()
        update_only = options.get('update_only')
        os.system('crowdin-cli -c %s download' % self.crowdin_config_path())
        if not update_only:
            call_command('compilemessages')

    def crowdin_config_path(self):
        return settings.ROOT_PATH + '/crowdin.yaml'

    def check_install(self):
        '''
        Check if the `crowdin-cli` command is installed
        '''
        crowdin_installed = os.system('which crowdin-cli > /dev/null') == 0
        config_file_created = os.path.exists(self.crowdin_config_path())
        if not crowdin_installed:
            raise CommandError('crowdin-cli doesn\'t seem to be installed, '\
                'please follow installation instructions from crowdin doc: '\
                'http://crowdin.net/page/cli-tool#download-cli-client')

        if not config_file_created:
            raise CommandError('The crowdin configuration file is missing, '\
                 'please add a file named crowdin.yaml at the root of this '\
                 'project or rename the crowdin.yaml.template to crowdin.yaml')
