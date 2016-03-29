import os
import io
import cProfile
import cv2
import requests
import pstats
import numpy as np
from matplotlib import pyplot as plt
from django.core.management.base import BaseCommand, CommandError
from image_api.imageloader import Imageloader
from image_query import query


class Command(BaseCommand):
    help = 'Query Image on CDN and Draw the Results'

    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            '--image',
            type=str,
            dest="img",
            help='The path to image')

        parser.add_argument(
            '-l',
            '--limit',
            default=40,
            type=int,
            dest="limit",
            nargs='?',
            help='Set output limits')

    def handle(self, *args, **options):
        if os.path.exists(options['img']):
            print('Searching image on local database')
            search = query.Search()
            pr = cProfile.Profile()
            pr.enable()
            results = search.search_image(cv2.imread(options['img']), bow_hist=None, color_hist=None, metric='chisqr_alt')
            pr.disable()
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats()
            print(s.getvalue())
            top = sorted(results, key=lambda element: (element[2], element[1]))[:options['limit']]
            print(top)
            print('Generating Results from CDN')
            plt.figure()
            plt.gray()
            plt.subplot(5,9,1)

            img = cv2.imread(options['img'])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.imshow(img)
            plt.axis('off')
            loader = Imageloader()
            j = 0
            for img_path, _, _ in top:
                i = requests.get(loader.get_url(img_path))
                nparr = np.fromstring(i.content, np.uint8)
                img = cv2.imdecode(nparr, 1)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                plt.gray()
                plt.subplot(5,9,j+5)
                j+=1
                plt.imshow(img)
                plt.axis('off')

            plt.show()
            self.stdout.write("Exiting...\n", ending='')
        else:
            self.stderr.write("Error Input Image\n", ending='')
