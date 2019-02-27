FROM zigzacks/zigdata:base

RUN pip install --upgrade lektor

COPY . blog

# setup s6 services
RUN mkdir -p /etc/services.d/lektor && \
    mv blog/lektor.run /etc/services.d/lektor/run

# expose the port
EXPOSE 8888
ENTRYPOINT ["/init"]
CMD []