import requests
from qiniu import Auth
from django.conf import settings

class imageloader:
    def get_url(self,img_path):
        base_url = 'http://%s/%s' % (self.QINIU_BUCKET_DOMAIN, img_path)
        private_url = self.q.private_download_url(base_url, expires=3600)
        r = requests.get(private_url)
        assert r.status_code == 200
        return private_url

    def __init__(self):
        self.QINIU_ACCESS_KEY = getattr(settings, 'QINIU_ACCESS_KEY', None)
        self.QINIU_SECRET_KEY = getattr(settings, 'QINIU_SECRET_KEY', None)
        self.QINIU_BUCKET_DOMAIN = getattr(settings, 'QINIU_BUCKET_DOMAIN', None)
        self.q = Auth(self.QINIU_ACCESS_KEY, self.QINIU_SECRET_KEY)
