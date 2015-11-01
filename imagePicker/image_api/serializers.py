from dbmanager.models import image
from rest_framework import serializers
from image_api.imageloader import imageloader


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    img_path = serializers.SerializerMethodField('rewrite')
    class Meta:
        model = image
        fields = ('img_path','key')

    def rewrite(self, img_path):
        loader = imageloader()
        return loader.get_url(img_path)
