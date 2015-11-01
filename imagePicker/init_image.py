#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imagePicker.settings")
from django.conf import settings
from dbmanager.models import image
from qiniu import Auth
from qiniu import BucketManager

ImageList = []
QINIU_ACCESS_KEY = getattr(settings, 'QINIU_ACCESS_KEY', None)
QINIU_SECRET_KEY = getattr(settings, 'QINIU_SECRET_KEY', None)
QINIU_BUCKET_DEFAULT = getattr(settings, 'QINIU_BUCKET_DEFAULT', None)

q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)

def store(image_name):
    img = image(img_path=image_name)
    ImageList.append(img)


def insert_all(bucket_name, bucket=None, prefix=None, limit=None):
    if bucket is None:
        bucket = BucketManager(q)
    marker = None
    eof = False
    while eof is False:
        ret, eof, info = bucket.list(bucket_name, prefix=prefix, marker=marker, limit=limit)
        marker = ret.get('marker', None)
        for item in ret['items']:
            print(item['key'])
            store(item['key'])
            pass
    if eof is not True:
        pass


def main():
    insert_all(QINIU_BUCKET_DEFAULT)
    image.objects.bulk_create(ImageList)

if __name__ == "__main__":
    main()
    print('Image DB initialize Done!')
