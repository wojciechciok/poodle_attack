from flask import Flask, request
from flask_cors import CORS
import binascii
from Crypto.Cipher import AES
import hmac
import hashlib

app = Flask(__name__)
CORS(app)


BLOCK_SIZE = 16
IV = b"secret_key_11111"
KEY = b"secret_key_11111"


def decrypt(ciphertext, p=False):
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_message = aes.decrypt(ciphertext)
    padding_len = decrypted_message[-1]
    message_no_padding = decrypted_message[:-padding_len]
    mac = message_no_padding[-32:]
    plaintext = message_no_padding[:-32]
    new_mac = hmac.new(KEY, plaintext, hashlib.sha256).digest()
    if new_mac == mac:
        return plaintext
    else:
        return 0


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
    app.run(port=5002, debug=True)
