from dbmanager.models import Image, Vocabulary


class Dumper(object):

    def __init__(self):
        imgs = Image.objects.all()
        self.img_data = []
        for img in imgs:
            self.img_data.append(
                (img.img_path, img.get_bow_hist(), img.get_color_hist()))
        self.voc = Vocabulary.objects.get().get_data()

    def get_img_data(self):
        return self.img_data

    def get_voc_data(self):
        return self.voc
