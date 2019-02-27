# let's use this compact miniconda, alpine based image
FROM frolvlad/alpine-miniconda3

# gcc dependencies and such
RUN apk add --no-cache bash curl ca-certificates git openssh nginx
ENV HOME /usr/local/zigdata.org
RUN mkdir -p $HOME

WORKDIR $HOME
COPY env.yaml .

# set up conda env
RUN apk add --no-cache gcc musl-dev build-base
RUN conda env create -f env.yaml && source activate zigdata

# expose the port
EXPOSE 8888

ADD https://github.com/just-containers/s6-overlay/releases/download/v1.21.8.0/s6-overlay-amd64.tar.gz /tmp/
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C /

# nginx
RUN adduser -D -g 'www' www && \
    mkdir /www && \
    chown -R www:www /var/lib/nginx && \
    chown -R www:www /www

COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/index.html /www/index.html
COPY reddit-headline-extractor.py .
COPY services .

# setup s6 services
RUN mkdir -p /etc/services.d/jupyter && \
    cp jupyter.run /etc/services.d/jupyter/run && \
    mkdir -p /etc/services.d/reddit && \
    cp reddit.run /etc/services.d/reddit/run && \
    mkdir -p /etc/services.d/nginx && \
    cp nginx.run /etc/services.d/nginx/run && \
    rm -rf jupyterlab.run reddit.run nginx.run

ENTRYPOINT ["/init"]

ENV PATH /opt/conda/envs/zigdata/bin:$PATH
CMD []