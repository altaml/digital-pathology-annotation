FROM continuumio/miniconda3

RUN apt-get update
RUN apt-get install --yes openslide-tools python-pip wget sudo
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install pillow numpy openslide-python
ENV LD_LIBRARY_PATH /usr/local/lib
RUN conda update conda
RUN conda install pixman=0.36.0
RUN sudo mkdir -m 777 /usr/app
COPY . /usr/app
WORKDIR /usr/app
ENV PYTHONPATH=/usr/app
RUN pip install -e /usr/app
RUN pytest /usr/app/tests
