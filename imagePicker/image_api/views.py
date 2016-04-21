import cv2
import base64
import numpy as np
import msgpack
from image_query import query
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile
from image_api.render import VocRenderer
from dbmanager.models import Image
from dbmanager.models import Vocabulary
from image_api.serializers import ImageSerializer


search = query.Search()


@api_view(['POST'])
@silk_profile(name='Search Image')
def search_images(request):
    if 'limit' in request.query_params.keys():
        limit = int(request.query_params['limit'])
    else:
        limit = 10

    if 'method' in request.query_params.keys():
        method = request.query_params['method']
    else:
        method = None

    if 'disableBoW' in request.query_params.keys():
        disableBoW = True
    else:
        disableBoW = False

    try:
        if request.FILES.get("image", None) is not None:
            sketch = True if 'sketch' in request.query_params.keys() else False
            data = np.asarray(
                bytearray(request.FILES['image'].read()), dtype="uint8")
            img = cv2.imdecode(data, (-1 if sketch else cv2.IMREAD_COLOR))
            results = query.get_results(search.search_image(
                img, bow_hist=None, color_hist=None,
                metric=method, sketch=sketch), disableBoW)[:limit]
            imgs = Image.objects.in_bulk(results)
            sorted_imgs = [imgs[img_path] for img_path in results]
            serializer = ImageSerializer(sorted_imgs, many=True)
            return Response(serializer.data)

        else:

            bow_hist = base64.b64decode(request.data['bow_hist'])
            bow_hist = np.array(msgpack.unpackb(bow_hist), dtype=np.float32)
            color_hist = base64.b64decode(request.data['color_hist'])
            color_hist = np.array(msgpack.unpackb(color_hist), dtype=np.float32)
            results = query.get_results(search.search_image(
                img=None, bow_hist=bow_hist, color_hist=color_hist,
                metric=method), disableBoW)[:limit]
            imgs = Image.objects.in_bulk(results)
            sorted_imgs = [imgs[img_path] for img_path in results]
            serializer = ImageSerializer(sorted_imgs, many=True)
            return Response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@renderer_classes((VocRenderer,))
@silk_profile(name='Get Voc')
def get_voc(request):
    try:
        bow_voc = Vocabulary.objects.get().get_data()
        bow_voc = base64.b64encode(msgpack.packb(bow_voc.tolist()))
        return Response(bow_voc)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
