from flask import Flask, request
from flask_json import FlaskJSON, json_response
from api.models import ApiV1, ApiV2

app = Flask(__name__)
FlaskJSON(app)


@app.route('/api/<version:string>/order', methods=['POST'])
def api(version):
    apis = {'v1': 'ApiV1', 'v2': 'ApiV2'}
    api_class = apis[version]
    order = api_class(request.get_json())
    if order.check():
        order.save()
    return json_response(check=order.check())


if __name__ == '__main__':
    app.run(debug=True)
