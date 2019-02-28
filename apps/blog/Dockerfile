FROM zigzacks/zigdata:base

RUN pip install --upgrade lektor

COPY . blog

# setup s6 services
RUN mkdir -p /etc/services.d/lektor && \
    mv blog/lektor.run /etc/services.d/lektor/run

# nginx
RUN adduser -D -g 'www' www && \
    mkdir /www && \
    chown -R www:www /var/lib/nginx && \
    chown -R www:www /www

COPY nginx/nginx.conf /etc/nginx/nginx.conf

# expose the port
EXPOSE 80
ENTRYPOINT ["/init"]
CMD []