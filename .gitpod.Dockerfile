
FROM ubuntu:20.04

# basic libs
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y wget build-essential gcc zlib1g-dev libbz2-dev git curl xz-utils file sudo

# latest openssl for python
WORKDIR /root/
RUN wget https://www.openssl.org/source/openssl-1.1.1d.tar.gz \
        && tar zxf openssl-1.1.1d.tar.gz \
        && cd openssl-1.1.1d \
        && ./config \
        && make \
        && make install

# python
WORKDIR /root/
RUN wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz \
        && tar zxf Python-3.6.8.tgz \
        && cd Python-3.6.8 \
        && ./configure \
        && make altinstall
ENV PYTHONIOENCODING "utf-8"

WORKDIR /usr/local/bin/
RUN ln -s python3.6 python
RUN ln -s pip3.6 pip

# mecab
RUN apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8

# mecab-ipadi-NEologd
WORKDIR /root/
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
WORKDIR /root/mecab-ipadic-neologd
RUN ./bin/install-mecab-ipadic-neologd -n -y
RUN echo `mecab-config --dicdir`"/mecab-ipadic-neologd" > neologd.log

RUN cp /etc/mecabrc /usr/local/etc/mecabrc

# python app settings
# ADD requirements.txt ./requirements.txt
RUN pip install mecab-python3 gensim

WORKDIR /