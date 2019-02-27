FROM zigzacks/zigdata:base

COPY reddit-headline-extractor.py .
COPY reddit.run .

# setup s6 services
RUN mkdir -p /etc/services.d/reddit && \
    mv reddit.run /etc/services.d/reddit/run

ENTRYPOINT ["/init"]
CMD []