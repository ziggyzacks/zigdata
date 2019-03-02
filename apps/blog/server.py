from sanic import Sanic
from sanic.response import json, html

app = Sanic()

app.static('/', '/var/www/zigdata')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
