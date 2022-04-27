from flask import Flask, request
from main import decrypt
from flask_cors import CORS, cross_origin
import binascii

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def home():
    data_dict = request.json
    data = data_dict['query']
    try:
        data_decrypt = decrypt(binascii.unhexlify(data))
        if data_decrypt == 0:
            return 'Fail'
        else:
            return 'Success'
    except:
        return 'Error'


if __name__ == "__main__":
    app.run(debug=True)
