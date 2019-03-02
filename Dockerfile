# let's use this compact miniconda, alpine based image
FROM frolvlad/alpine-miniconda3

# gcc dependencies and such
RUN apk add --no-cache bash curl ca-certificates git openssh nginx certbot
ENV HOME /usr/local/zigdata.org
RUN mkdir -p $HOME

WORKDIR $HOME
COPY env.yaml .

# set up conda env
RUN apk add --no-cache gcc musl-dev build-base
RUN conda env create -f env.yaml && source activate zigdata

ADD https://github.com/just-containers/s6-overlay/releases/download/v1.21.8.0/s6-overlay-amd64.tar.gz /tmp/
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C /

ENV PATH /opt/conda/envs/zigdata/bin:$PATH