FROM zigzacks/zigdata:base

COPY jupyter.run .
COPY jupyter_notebook_config.py $HOME/.jupyter/

# setup s6 services
RUN mkdir -p /etc/services.d/jupyter && \
    mv jupyter.run /etc/services.d/jupyter/run

# expose the port
EXPOSE 8989
ENTRYPOINT ["/init"]
CMD []