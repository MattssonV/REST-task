from flask import Flask, request, jsonify

#

app = Flask(__name__)

def calc():

    return 0

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
