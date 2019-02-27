FROM zigzacks/zigdata:base

RUN pip install redis

COPY reddit-headline-extractor.py .
COPY reddit.run .

# setup s6 services
RUN mkdir -p /etc/services.d/reddit && \
    mv reddit.run /etc/services.d/reddit/run

EXPOSE 6379

ENTRYPOINT ["/init"]
CMD []