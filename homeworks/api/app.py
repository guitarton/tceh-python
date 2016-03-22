from flask import Flask, request
from flask_json import FlaskJSON, json_response
from api.models import ApiV1, ApiV2

app = Flask(__name__)
FlaskJSON(app)


@app.route('/api/v1/order', methods=['POST'])
def api_v1():
    order = ApiV1(request.get_json())
    if order.check():
        order.save()
    return json_response(check=order.check())


@app.route('/api/v2/order', methods=['POST'])
def api_v2():
    order = ApiV2(request.get_json())
    if order.check():
        order.save()
    return json_response(check=order.check())


if __name__ == '__main__':
    app.run(debug=True)
