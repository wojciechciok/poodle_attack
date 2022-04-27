from flask import Flask, request
from flask_cors import CORS
import requests
import json

app2 = Flask(__name__)
CORS(app2)


@app2.route("/part1", methods=["POST"])
def part1():
    data_dict = request.json
    data = data_dict['query']  # <- this is the message from client
    return 'ok'


@app2.route("/part2", methods=["POST"])
def part2():

    # get the message
    data_dict = request.json
    data = data_dict['query']  # <- this is the message from client

    # make request to server
    headers = {'Content-type': 'application/json'}
    response_object = requests.post('http://127.0.0.1:5002/',
                                    data=json.dumps({"query": data}), headers=headers)
    response_text = response_object.text
    return response_text  # <- this is response from server


if __name__ == "__main__":
    app2.run(port=5001, debug=True)
