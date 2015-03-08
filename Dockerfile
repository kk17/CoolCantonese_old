FROM kk17/ekho
MAINTAINER Zhike Chan "zk.chan007@gmail.com"
ENV REFRESHED_AT 2015-3-7

## Install ffmpeg.
RUN \
  add-apt-repository ppa:jon-severinsson/ffmpeg && \
  apt-get update && \
  apt-get -y install ffmpeg && \
  rm -rf /var/lib/apt/lists/*

## Install Python.
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*

## Install Python packages.
COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r requirements.txt && rm -rf requirements.txt

VOLUME ["/Cantonese","/Cantonese_audio"]
WORKDIR /Cantonese

ENTRYPOINT []
CMD []