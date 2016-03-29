from django.core.management.base import BaseCommand, CommandError
from initializer.init_db import db_initializer


class Command(BaseCommand):
    help = 'Compute BoW Vocabulary, BoW Histogram, Color Histogram'

    def add_arguments(self, parser):
        parser.add_argument(
            '-t',
            '--type',
            type=str,
            dest = "type",
            help='Compute type (voc, hist)')

        parser.add_argument(
            '-p',
            '--path',
            default='../tmp',
            type=str,
            dest = "dir",
            nargs='?',
            help='Set download folder')

        parser.add_argument(
            '-l',
            '--limit',
            default=1000,
            type=int,
            dest = "limit",
            nargs='?',
            help='Set compute limits')

    def handle(self, *args, **options):
        init = db_initializer(options['dir'])
        if options['type'] == 'voc':
            print('Computing BoW Vocabulary')
            init.compute_voc(options['limit'])
            self.stdout.write("Finish Compute BoW Vocabulary\n", ending='')
        elif options['type'] == 'hist':
            print('Computing Histogram')
            init.compute_hist()
            self.stdout.write("Finish Compute Histogram\n", ending='')
        else:
            self.stderr.write("Error Input Argument\n", ending='')
