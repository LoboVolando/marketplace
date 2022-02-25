import os

from django.core import management
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from config.settings import INSTALLED_APPS, DATABASES
try:
    from config.settings import FOLDER_FIXTURES
except ImportError:
    FOLDER_FIXTURES = 'fixtures'


class Command(BaseCommand):
    help = 'Run all migrations and load fixtures'

    def add_arguments(self, parser):
        parser.add_argument('with_clear', type=str, help='Delete only migrations files. '
                                                         'Set "no_clear" for cancel deleting')
        # Optional argument
        parser.add_argument('--db', action='store_true', help='Prefix for deleting database', )

    def handle(self, *args, **kwargs):
        fixtures_list = self._get_list_fixtures()
        err_list = list()
        n_iteration = len(fixtures_list) * 2

        if kwargs['with_clear'] == 'with_clear':
            self._remove_old_migrations()
        if kwargs['db']:
            self._remove_database()
        management.call_command('makemigrations')
        management.call_command('migrate')
        management.call_command('new_site_name')
        self.stdout.write(f'\nFIXTURES LOAD...')
        while fixtures_list:
            err_list.clear()
            for item in fixtures_list:
                self.stdout.write(f'Loading {item}')
                try:
                    management.call_command('loaddata', os.path.normpath(os.path.join(FOLDER_FIXTURES, item)))
                    fixtures_list.remove(item)
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(f'IntegrityError when loading {item}'))
                    err_list.append(item)
            if n_iteration == 0:
                break
            n_iteration -= 1

        if err_list:
            self.stdout.write(self.style.WARNING(f'Not all fixtures have been loaded. Check it:'))
            self.stdout.write(self.style.WARNING(err_list))
        else:
            self.stdout.write(self.style.SUCCESS(f'\nAll commands and loadings have been successful!'))

    def _remove_old_migrations(self):
        self.stdout.write(f'\nRemove old migration files...\n')
        list_apps = self._get_apps_list()
        for item in list_apps:
            path = os.path.join(os.path.abspath(item), 'migrations')
            for file in os.listdir(path):
                if not file.startswith('__'):
                    os.remove(os.path.join(path, file))

    def _remove_database(self):
        self.stdout.write(f'\nRemove database...\n')
        path_db = DATABASES['default']['NAME']
        if os.path.exists(path_db):
            os.remove(path_db)
        else:
            self.stdout.write(self.style.WARNING(f'Database file {path_db} does not exist.\n'))

    def _get_list_fixtures(self):
        path_fixtures = os.path.normpath(os.path.abspath(FOLDER_FIXTURES))
        if os.path.exists(path_fixtures):
            return os.listdir(path_fixtures)
        return []

    def _get_apps_list(self):
        list_apps = []
        for item in INSTALLED_APPS:
            path = os.path.join(os.path.abspath(item), 'migrations')
            if os.path.exists(path):
                list_apps.append(item)
        return list_apps
