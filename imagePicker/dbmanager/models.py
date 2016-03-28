import pickle
from django.db import models
from solo.models import SingletonModel

# Create your models here.
class Image(models.Model):
    img_path = models.CharField(max_length=200, primary_key=True)
    bow_hist = models.BinaryField(null=True)
    color_hist = models.BinaryField(null=True)

    def set_bow_hist(img, bow_hist):
        data = pickle.dumps(bow_hist)
        Image.objects.filter(img_path=img).update(bow_hist=data)

    def set_color_hist(img, color_hist):
        data = pickle.dumps(color_hist)
        Image.objects.filter(img_path=img).update(color_hist=data)

    def get_bow_hist(self):
        return pickle.loads(self.bow_hist)

    def get_color_hist(self):
        return pickle.loads(self.color_hist)

    def __str__(self):
        return self.img_path

class Vocabulary(SingletonModel):
    bow_voc = models.BinaryField(null=True)

    def set_data(data):
        bow_voc = pickle.dumps(data)
        if Vocabulary.objects.exists():
            Vocabulary.objects.update(bow_voc=bow_voc)
        else:
            Vocabulary.objects.create(bow_voc=bow_voc)

    def get_data(self):
        return pickle.loads(self.bow_voc)
