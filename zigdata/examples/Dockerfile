FROM zigzacks/zigdata:base

COPY nginx.run .
COPY nginx.conf /etc/nginx/nginx.conf
COPY cli.ini /etc/letsencrypt/cli.ini
COPY dhparam.pem /certs/dhparam.pem
COPY index.html /usr/share/nginx/html

# setup s6 services
RUN mkdir -p /etc/services.d/nginx && \
    mv nginx.run /etc/services.d/nginx/run

# nginx
RUN adduser -D -g 'www' www && \
    mkdir -p /www && \
    mkdir -p /var/www/zigdata && \
    chown -R www:www /var/lib/nginx && \
    chown -R www:www /www

# expose the port
EXPOSE 80
EXPOSE 8888
EXPOSE 443
ENTRYPOINT ["/init"]
CMD []