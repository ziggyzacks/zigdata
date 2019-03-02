FROM zigzacks/zigdata:base

RUN pip install --upgrade lektor sanic gunicorn

COPY . blog
COPY server.py .
COPY wsgi.py .

# setup s6 services
RUN mkdir -p /etc/services.d/gunicorn && \
    mv blog/gunicorn.run /etc/services.d/gunicorn/run && \
    mkdir -p /etc/services.d/nginx && \
    mv blog/nginx.run /etc/services.d/nginx/run

# nginx
RUN adduser -D -g 'www' www && \
    mkdir /www && \
    mkdir -p /var/www/media/images/ && \
    cp blog/favicon.ico /var/www/media/images/favicon.ico && \
    chown -R www:www /var/lib/nginx && \
    chown -R www:www /www

COPY nginx/nginx.conf /etc/nginx/nginx.conf

# expose the port
EXPOSE 80
EXPOSE 8888
EXPOSE 8080
EXPOSE 443

ENTRYPOINT ["/init"]
CMD []