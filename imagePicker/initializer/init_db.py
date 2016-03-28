import os
import requests
import threading
import numpy as np
from queue import Queue
from algolib import populator
from dbmanager.models import Image, Vocabulary
from image_api.imageloader import Imageloader


class db_initializer(object):

    def __init__(self, directory='../tmp'):
        self.img_list = Image.objects.all()
        self.loader = Imageloader()
        self.directory = directory
        self.populator = populator.Populator()

    def image_queue(self, imgs):
        img_queue = Queue()
        for i in imgs:
            img_queue.put(i.img_path)
        return img_queue

    def download_img(self, loader, img_queue, directory='../tmp'):
        while not img_queue.empty():
            i = img_queue.get()
            try:
                img = requests.get(loader.get_url(i))
                path = os.path.join(directory, i)
                f = open(path, 'wb')
                f.write(img.content)
                f.close()
                print('Save file ', i)
            except IOError:
                print('Failed save file: ', i, 'IOError.')

    def getimages(self):
        print('Start Downloading Images')
        if os.path.exists(self.directory):
            print('The Directory is not Empty !')
            exit()
        os.makedirs(self.directory)
        img_queue = self.image_queue(self.img_list)
        for _ in range(10):
            t = threading.Thread(
                target=self.download_img(self.loader, img_queue, self.directory))
            t.start()
        print('Database Initialization Done!')

    def compute_voc(self, limit=1000):
        imgs = populator.list_images(self.directory)
        Vocabulary.set_data(self.populator.generate_vocabulary(imgs, limit))

    def compute_hist(self):
        bow_voc = Vocabulary.objects.get().get_data()
        imgs = populator.list_images(self.directory)
        for path, img in imgs:
            print(path)
            bow_hist = self.populator.bow_hist(img, bow_voc)
            color_hist = self.populator.color_hist(img)
            _, img_path = os.path.split(path)
            Image.set_bow_hist(img_path, bow_hist)
            Image.set_color_hist(img_path, color_hist)
