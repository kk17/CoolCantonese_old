FROM kk17/coolcantonese
MAINTAINER Zhike Chan "zk.chan007@gmail.com"
ENV REFRESHED_AT 2015-4-7

#copy codes
COPY ./ /Cantonese

EXPOSE 80

ENTRYPOINT ["python"]
CMD ["wechat.py", "-e", "Pro"]