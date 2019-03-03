FROM zigzacks/zigdata:base

COPY jupyter.run .
COPY jupyter_notebook_config.py $HOME/.jupyter/
COPY ../blog/zigdata/assets/static/img/favicon.ico .

# setup s6 services
RUN mkdir -p /etc/services.d/jupyter && \
    mv jupyter.run /etc/services.d/jupyter/run


# nginx
RUN adduser -D -g 'www' www && \
    mkdir /www && \
    mkdir -p /var/www/media/images/ && \
    cp favicon.ico /var/www/media/images/favicon.ico && \
    chown -R www:www /var/lib/nginx && \
    chown -R www:www /www

COPY nginx/nginx.conf /etc/nginx/nginx.conf

# expose the port
EXPOSE 80
EXPOSE 443
ENTRYPOINT ["/init"]
CMD []