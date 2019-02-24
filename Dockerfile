# let's use this compact miniconda, alpine based image
FROM frolvlad/alpine-miniconda3

# gcc dependencies and such
RUN apk add --no-cache bash curl build-base ca-certificates git openssh
RUN apk add --no-cache --virtual .build-deps gcc musl-dev
ENV HOME /usr/local/zigdata.org
RUN mkdir -p $HOME
WORKDIR $HOME
COPY . .
# set up conda env
RUN conda env create -f env.yaml
RUN source activate zigdata
RUN apk del .build-deps gcc musl-dev
# expose the port
EXPOSE 8686
# let's supervise with s6
ADD https://github.com/just-containers/s6-overlay/releases/download/v1.21.8.0/s6-overlay-amd64.tar.gz /tmp/
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C /
ENTRYPOINT ["/init"]
# fire up jupyterlab
CMD ["jupyterlab",  "--no-browser", "--port 8686", "--host 0.0.0.0"]