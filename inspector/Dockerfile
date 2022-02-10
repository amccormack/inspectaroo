FROM ubuntu:impish
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
    python3 python3-dev python3-pip libimage-exiftool-perl \
    curl unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

WORKDIR /src

ADD requirements.txt /src/
RUN pip install -r requirements.txt

ADD app.py /src/