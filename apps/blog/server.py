from sanic import Sanic
from sanic.response import json, html

app = Sanic()


@app.route('/json')
async def api_route(request):
    return json({'hello': 'world'})


@app.route('/')
def frontend_route(request):
    return html('<p>Hello world!</p>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
