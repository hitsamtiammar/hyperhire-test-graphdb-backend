from server import app
from flask import request

@app.route('/')
def index():
    return {"Data": "12345"}

@app.route('/post', methods=['POST'])
def post():
    print('Hello 12345 44444')
    return {'Data': 'This is post example', 'd': request.json['Hello'] + 'Lalalal'}