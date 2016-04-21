from algolib.query import Query
from initializer.data_dumper import Dumper


class Search(object):

    def __init__(self):
        self.dumper = Dumper()
        self.query = Query()

    def search_image(self, img, bow_hist, color_hist, metric, sketch=False):
        return self.query.query_image(img, bow_hist, color_hist, self.dumper.get_img_data(), self.dumper.get_voc_data(), metric, sketch)

def get_results(results):
    imgs = []
    results = sorted(results, key=lambda element: (element[2], element[1]))
    for img, _, _ in results:
        imgs.append(img)
    return imgs
