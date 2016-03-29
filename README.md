## Image-Picker

This is the backend service of InstaSketch application, based on Django framework. A RESTful web server combine with CBIR engine.

### How to Hack

#### Basic Requirement

Python >= 3.5, Opencv3.1.0 with extra contrib modules

#### Getting Start

Before start, make sure you set all environment variables in `imagePicker/settings.py`, then :

```

pip install -r imagePicker/requirements.txt

cd imagePicker && python manage.py runserver

```

Access http://localhost:8000/ to verify if it works.

#### Initialization

Initialize Database Image Set :

`python init_image.py`

Download Images form CDN, use `-p` `--path` to set the location :

`cd imagePicker && python manage.py download -p ./tmp/`

Compute BOVW K-Mean Cluster Centre, use `-p` to specify image path, `-l` for calculation limits :

`cd imagePicker && python manage.py -t voc -p ./tmp/  -l 1000`

Compute BOVW Histogram and Color Histogram :

`cd imagePicker && python manage.py -t hist -p ./tmp/`

### API Usage

Currently the image query api support POST by image histogram or POST by image itself

- POST Image Python Example :

```

import requests

url = 'http://127.0.0.1:8000/images/'
files = {'image': open('test/1.jpg', 'rb')}
args = {'limit': 20, 'method': 'chisqr_alt'}
r = requests.post(url, files=files, params=args)
print(r.text)

```

- POST Image Histogram Python Example :

```

import requests
import base64
import cv2
import numpy as np
from algolib.populator import Populator

url = 'http://127.0.0.1:8000/vocabulary/'
s = base64.b64decode(requests.get(url).text)
voc = np.fromstring(s, dtype=np.float32).reshape((200,128))

pop = Populator()
img = cv2.imread('test/1.jpg')
bow_hist = pop.bow_hist(img, voc)
color_hist = pop.color_hist(img)

bow_hist = base64.b64encode(bow_hist.tostring())
color_hist = base64.b64encode(color_hist.tostring())

url = 'http://127.0.0.1:8000/images/'
args = {'limit': 20, 'method': 'chisqr_alt'}
data = {'bow_hist':bow_hist, 'color_hist':color_hist}
r = requests.post(url, data=data, params=args)
print(r.text)


```
