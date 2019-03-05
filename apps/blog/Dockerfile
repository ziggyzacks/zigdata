FROM zigzacks/zigdata:base

RUN pip install --upgrade lektor sanic gunicorn

COPY . blog

# setup s6 services
RUN mkdir -p /etc/services.d/blog && \
    mv blog/blog.run /etc/services.d/blog/run

# expose the port
EXPOSE 8888

ENTRYPOINT ["/init"]
CMD []