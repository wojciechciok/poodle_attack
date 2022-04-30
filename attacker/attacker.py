from flask import Flask, request
from flask_cors import CORS
import requests
import json
import binascii
import hashlib
import hmac
from Crypto import Random
from Crypto.Cipher import AES
import json

app2 = Flask(__name__)
CORS(app2)

url_length = 34

fill_length = 0
original_length = 0
BLOCK_SIZE = 16
block_to_guess = 0
byte_in_block_to_guess = 0

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

@app2.route("/part1", methods=["POST"])
def part1():
    data_dict = request.json
    data = data_dict['query']  # <- this is the message from client
    global original_length
    global fill_length
    global block_to_guess

    length = len(data)
    if(original_length == 0):
        original_length = length
        block_to_guess = (original_length // 32 - 2)
    
    if(length > original_length):
        print(fill_length)
        return str(length)
    fill_length += 1
    return str(length)

@app2.route("/key", methods=["GET"])
def getNextKey():
    global KEY
    global IV
    response_object = requests.get('http://127.0.0.1:5002/key')

    response_text = response_object.text
    KEY = json.loads(response_text)["key"].encode()
    IV = json.loads(response_text)["iv"].encode()
    return response_text

def decrypt(ciphertext):
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


@app2.route("/part2", methods=["POST"])
def part2():

    # get the message
    data_dict = request.json
    data = data_dict['query']  # <- this is the message from client
    global block_to_guess
    global byte_in_block_to_guess

    if byte_in_block_to_guess >= 16:
        byte_in_block_to_guess = 0
        block_to_guess -= 1

    encrypted_message_blocks = [data[i:i + 32] for i in
                                    range(0, len(data), 32)]

    # Substitute the last block (the padding block) with the block we want to decrypt
    encrypted_message_blocks[-1] = encrypted_message_blocks[block_to_guess]

    data = "".join(encrypted_message_blocks)
    # print("Data:")
    # print(data)
    # Check if the last byte of the substituted block makes a correct padding:
    # make request to server
    headers = {'Content-type': 'application/json'}
    response_object = requests.post('http://127.0.0.1:5002/',
                                    data=json.dumps({"query": data}), headers=headers)
    response_text = response_object.text
    # If the padding is correct (the last byte of the deciphered block is 15 = 0f)

    if response_text != "Fail":
        # Get the last byte of the last block of mac - block before the one that we are deciphering
        last_mac_block = encrypted_message_blocks[-2]
        # Get the block before the secret block
        first_block = encrypted_message_blocks[block_to_guess - 1]
        # Get the deciphered last byte
        deciphered_byte = chr(int("0f", 16) ^ int(
            last_mac_block[-2:], 16) ^ int(first_block[-2:], 16))
        byte_in_block_to_guess += 1

        print("Success")
        print(deciphered_byte)

        return deciphered_byte

    elif response_text == "Error":
        return "Error"  # <- this is response from server

    return "Failure"


if __name__ == "__main__":
    
    app2.run(port=5001, debug=True)
