from flask import Flask, request
from main import decrypt

app = Flask(__name__)

@app.route("/", methods=["POST"])
def home():
    data_dict = request.json
    data = data_dict['query']
    data_decrypt = decrypt(data)
    if data_decrypt == 0:
        return 'Fail'
    else:
        return 'Success'

if __name__ == "__main__":
    app.run(debug=True)