FROM zigdata:base

COPY jupyter.run .

# setup s6 services
RUN mkdir -p /etc/services.d/jupyter && \
    mv jupyter.run /etc/services.d/jupyter/run

# expose the port
EXPOSE 8888
ENTRYPOINT ["/init"]
CMD []