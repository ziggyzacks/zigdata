FROM zigzacks/zigdata:base

RUN pip install --upgrade lektor sanic gunicorn

COPY . blog
COPY server.py .
COPY wsgi.py .

# setup s6 services
RUN mkdir -p /etc/services.d/gunicorn && \
    mv blog/gunicorn.run /etc/services.d/gunicorn/run

# expose the port
EXPOSE 8888

ENTRYPOINT ["/init"]
CMD []