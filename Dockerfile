# let's use this compact miniconda, alpine based image
FROM frolvlad/alpine-miniconda3

# gcc dependencies and such
RUN apk add --no-cache bash curl ca-certificates git openssh
ENV HOME /usr/local/zigdata.org
RUN mkdir -p $HOME

WORKDIR $HOME
COPY env.yaml .
COPY reddit.py .
COPY services .

# setup s6 services
RUN mkdir -p /etc/services.d/jupyterlab && \
    cp jupyterlab.run /etc/services.d/jupyterlab/run && \
    mkdir -p /etc/services.d/reddit && \
    cp reddit.run /etc/services.d/reddit/run && \
    rm -rf jupyterlab.run reddit.run

# set up conda env
RUN apk add --no-cache --virtual .build-deps gcc musl-dev build-base && \
    conda env create -f env.yaml && \
    source activate zigdata && \
    apk del .build-deps gcc musl-dev build-base && \
    rm -rf /opt/conda/pkgs/*

# expose the port
EXPOSE 8686

ADD https://github.com/just-containers/s6-overlay/releases/download/v1.21.8.0/s6-overlay-amd64.tar.gz /tmp/
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C /
ENTRYPOINT ["/init"]

ENV PATH /opt/conda/envs/zigdata/bin:$PATH
# fire up jupyterlab
CMD []