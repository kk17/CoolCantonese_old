FROM dockerfile/ubuntu
MAINTAINER Zhike Chan "zk.chan007@gmail.com"
ENV REFRESHED_AT 2015-2-27

## use mirror source
# RUN sed 's/archive\.ubuntu\.com/mirrors\.zju\.edu\.cn/' -i /etc/apt/sources.list

## Install ffmpeg.
RUN \
  add-apt-repository -y ppa:jon-severinsson/ffmpeg && \
  apt-get -qq update && \
  apt-get -qqy install ffmpeg

## Install ekho.
RUN \
  add-apt-repository -y ppa:hgneng/ekho && \
  apt-get -qq update && \
  apt-get -qqy install ekho

## remove apt cache
RUN  rm -rf /var/lib/apt/lists/*

## Install Python packages.
COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r requirements.txt && rm -rf requirements.txt

VOLUME ["/Cantonese","/Cantonese_audio"]
WORKDIR /Cantonese

# ENTRYPOINT ["wechat.py"]
# CMD ["-h"]