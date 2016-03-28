FROM python:3.5.1
MAINTAINER Dylan Wang <wanghaoyu@frazil.me>

RUN apt-get update
RUN apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libjasper-dev \
        libavformat-dev \
        libpq-dev \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        gfortran \
        nginx \
        libpq-dev \
        supervisor

RUN pip3 install uwsgi numpy

RUN wget https://github.com/Itseez/opencv/archive/3.1.0.zip
RUN wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
RUN unzip 3.1.0.zip \
&& unzip opencv_contrib.zip \
&& mkdir /opencv-3.1.0/cmake_binary \
&& cd /opencv-3.1.0/cmake_binary \
&& cmake -DBUILD_TIFF=ON \
  -DBUILD_opencv_java=OFF \
  -DWITH_CUDA=OFF \
  -DENABLE_AVX=ON \
  -DWITH_OPENGL=ON \
  -DWITH_OPENCL=ON \
  -DWITH_IPP=ON \
  -DWITH_TBB=ON \
  -DWITH_EIGEN=ON \
  -DWITH_V4L=ON \
  -DBUILD_TESTS=OFF \
  -DBUILD_PERF_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=RELEASE \
  -DOPENCV_EXTRA_MODULES_PATH=/opencv_contrib-3.1.0/modules \
  -DCMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
  -DPYTHON_EXECUTABLE=$(which python3) \
  -DPYTHON_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -DPYTHON_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") .. \
&& make install \
&& rm /3.1.0.zip \
&& rm -r /opencv-3.1.0

ADD imagePicker/requirements.txt /opt/django/requirements.txt
RUN pip3 install -r /opt/django/requirements.txt
ADD confs/* /opt/django/

RUN (echo "daemon off;" >> /etc/nginx/nginx.conf &&\
  rm /etc/nginx/sites-enabled/default &&\
  ln -s /opt/django/django.conf /etc/nginx/sites-enabled/ &&\
  ln -s /opt/django/supervisord.conf /etc/supervisor/conf.d/)

ADD static /opt/django/volatile/static/
ADD imagePicker /opt/django/app/


EXPOSE 80
CMD ["/opt/django/run.sh"]
