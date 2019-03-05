FROM zigzacks/zigdata:base

COPY . viz

# setup s6 services
RUN mkdir -p /etc/services.d/viz && \
    mv viz/viz.run /etc/services.d/viz/run

# expose the port
EXPOSE 8787

ENTRYPOINT ["/init"]
CMD []