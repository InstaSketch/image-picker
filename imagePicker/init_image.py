import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imagePicker.settings")
import django
django.setup()

from qiniu import Auth
from qiniu import BucketManager
from django.conf import settings
from dbmanager.models import Image

imagelist = []
QINIU_ACCESS_KEY = getattr(settings, 'QINIU_ACCESS_KEY', None)
QINIU_SECRET_KEY = getattr(settings, 'QINIU_SECRET_KEY', None)
QINIU_BUCKET_DEFAULT = getattr(settings, 'QINIU_BUCKET_DEFAULT', None)

q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)


def store(image_name):
    img = Image(img_path=image_name)
    imagelist.append(img)


def insert_all(bucket_name, bucket=None, prefix=None, limit=None):
    if bucket is None:
        bucket = BucketManager(q)
    marker = None
    eof = False
    while eof is False:
        buck = bucket.list(
            bucket_name, prefix=prefix, marker=marker, limit=limit)
        ret = buck[0]
        eof = buck[1]
        marker = ret.get('marker', None)
        for item in ret['items']:
            print(item['key'])
            store(item['key'])
    if eof is not True:
        pass


def main():
    insert_all(QINIU_BUCKET_DEFAULT)
    Image.objects.bulk_create(imagelist)

if __name__ == "__main__":
    main()
    print('Image Initialization Done!')
