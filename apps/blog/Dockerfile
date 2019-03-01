FROM zigzacks/zigdata:base

RUN pip install --upgrade lektor sanic

COPY . blog
COPY server.py .

# setup s6 services
RUN mkdir -p /etc/services.d/sanic && \
    mv blog/sanic.run /etc/services.d/sanic/run

# nginx
RUN adduser -D -g 'www' www && \
    mkdir /www && \
    mkdir -p /var/www/media/images/ && \
    cp blog/favicon.ico /var/www/media/images/favicon.ico && \
    chown -R www:www /var/lib/nginx && \
    chown -R www:www /www

COPY nginx/nginx.conf /etc/nginx/nginx.conf

# expose the port
EXPOSE 8888
ENTRYPOINT ["/init"]
CMD []