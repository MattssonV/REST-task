from flask import Flask, jsonify

app = Flask(__name__)

#@app.route('/example', methods=['GET'])
@app.route('/', methods=['GET'])
def example():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    return jsonify(data)