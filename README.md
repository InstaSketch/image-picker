## Image-Picker

This is the backend service of InstaSketch application, based on Django framework. It work with a RESTful web server combine CBIR engine.

### Before Start

Please go through those tutorials below to have a general concept:
  - Python Guide https://github.com/kennethreitz/python-guide
  - Django https://docs.djangoproject.com/en/1.8/intro/
  - Django REST framework http://www.django-rest-framework.org/#tutorial
  - OpenCV library http://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/


### How to Hack

#### Basic Requirement

python 2.7.x

#### For developers

Make sure command `python` and `pip` work on your machine.

Clone this repository, run `pip install -r imagePicker/requirements.txt` in your terminal.

`cd imagePicker && python manage.py runserver`

Access http://localhost:8000/ to verify if it works.


#### For non-developers

Install `docker` on your OS, https://www.docker.com/toolbox

After installation, make sure command `docker` is working.

Clone this repository, run `docker build -t image-picker .`

Build should successfully pass unless there is network issue.

Then run (replace `PATH_TO_YOUR_REPOSITORY` to your system path):

```  

docker run -p 80:80 -d -e MODULE=imagePicker -v /PATH_TO_YOUR_REPOSITORY/image-picker/imagePicker:/opt/django/app -v /PATH_TO_YOUR_REPOSITORY/image-picker/static:/opt/django/volatile/static image-picker

```
Access http://localhost/ to verify if it works.
