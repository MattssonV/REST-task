from flask import Flask, request, jsonify

# Use value of closing time prior day to calculate percentage increase/decrease

app = Flask(__name__)

def calc_change():
    return new/old*100

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
