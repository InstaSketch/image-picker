import os
from django.core.management.base import BaseCommand, CommandError
from initializer.init_db import db_initializer


class Command(BaseCommand):
    help = 'Download images from CDN to given folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            default='../tmp',
            type=str,
            dest = "dir",
            nargs='?',
            help='Set download folder')

    def handle(self, *args, **options):
        init = db_initializer(options['dir'])
        print('Images save to ', os.path.join(options['dir']))
        init.getimages()
        self.stdout.write("Finish Download\n", ending='')
