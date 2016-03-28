from dbmanager.models import Image
from rest_framework import serializers
from image_api.imageloader import Imageloader


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    img_path = serializers.SerializerMethodField('rewrite')
    class Meta:
        model = Image
        fields = ['img_path']

    def rewrite(self, img_path):
        loader = Imageloader()
        return loader.get_url(img_path)
