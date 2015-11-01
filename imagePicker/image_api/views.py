from django.shortcuts import render
from dbmanager.models import image
from rest_framework import viewsets
from image_api.serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = image.objects.all().order_by('img_path')
    serializer_class = ImageSerializer
