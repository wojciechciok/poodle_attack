from flask import Flask, request
from flask_cors import CORS
import binascii
from Crypto.Cipher import AES
from Crypto import Random
import hmac
import json
import hashlib

app = Flask(__name__)
CORS(app)

BLOCK_SIZE = 16
IV = b"secret_key_11111"
KEY = b"secret_key_11111"

# generate random key and iv


def generate_key():
    global IV
    byte_iv = Random.new().read(int(BLOCK_SIZE/2))
    IV = binascii.hexlify(byte_iv)
    global KEY
    byte_key = Random.new().read(int(BLOCK_SIZE/2))
    KEY = binascii.hexlify(byte_key)
    return


def decrypt(ciphertext):
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_message = aes.decrypt(ciphertext)
    padding_len = decrypted_message[-1] + 1
    message_no_padding = decrypted_message[:-padding_len]
    mac = message_no_padding[-32:]
    plaintext = message_no_padding[:-32]
    new_mac = hmac.new(KEY, plaintext, hashlib.sha256).digest()
    if new_mac == mac:
        return plaintext
    else:
        return 0


@app.route("/key", methods=["GET"])
def getNextKey():
    generate_key()
    response = json.dumps({"key": KEY.decode(), "iv": IV.decode()})
    return response


@app.route("/", methods=["POST"])
def home():
    data_dict = request.json
    data = data_dict['query']
    try:
        # print("data:")
        # print(data)
        # print("key:")
        # print(KEY)
        # print("iv:")
        # print(IV)
        data_decrypt = decrypt(binascii.unhexlify(data))
        # print(data_decrypt)
        if data_decrypt == 0:
            return 'Fail'
        else:
            return data_decrypt
    except:
        return 'Error'


if __name__ == "__main__":
    app.run(port=5002, debug=True)
