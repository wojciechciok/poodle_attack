from Crypto.Cipher import AES
import hmac
import hashlib

COOKIE = 'hello_there'
BLOCK_SIZE = 16
KEY = bytes([1] * BLOCK_SIZE)
IV = bytes([2] * BLOCK_SIZE)


def add_padding(message):
    message_len = len(message)
    padding_len = BLOCK_SIZE - (message_len % BLOCK_SIZE)
    last_byte = padding_len.to_bytes(1, 'big')
    result = message + bytes([0] * (padding_len-1)) + last_byte
    return result


def encrypt(plaintext):
    mac = hmac.new(KEY, plaintext, hashlib.sha256).digest()
    message = plaintext + mac
    padded_message = add_padding(message)
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    return aes.encrypt(padded_message)


def decrypt(cyphertext):
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_message = aes.decrypt(cyphertext)
    padding_len = decrypted_message[-1]
    message_no_padding = decrypted_message[:-padding_len]
    mac = message_no_padding[-32:]
    plaintext = message_no_padding[:-32]
    new_mac = hmac.new(KEY, plaintext, hashlib.sha256).digest()
    print(new_mac == mac)
    return plaintext


enc = encrypt(b'hello11')
decrypt(enc)
