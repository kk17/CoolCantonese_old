FROM ubuntu:14.04
MAINTAINER Zhike Chan "zk.chan007@gmail.com"
ENV REFRESHED_AT 2015-2-20
RUN apt-get -qq update

# Install ekho.
RUN \
  apt-get -qqy install software-properties-common && \
  add-apt-repository ppa:hgneng/ekho && \
  apt-get -qq update && \
  apt-get -qqy install ekho

# Install libav.
RUN apt-get -qqy install libav-tools

# Install Python.
RUN \
  apt-get -qq update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*

# Install Python packages.
COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip install -r requirements.txt && rm -rf requirements.txt

VOLUME ["/Cantonese","/Cantonese_audio"]
WORKDIR /Cantonese

#ENTRYPOINT ["wechat.py"]
#CMD ["-h"]