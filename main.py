from Crypto.Cipher import AES
from Crypto import Random
import hmac
import hashlib
import binascii
import re

COOKIE = 'Did you ever hear the tragedy of Darth Plagueis The Wise?'
BLOCK_SIZE = 16
IV = b"secret_key_11111"
KEY = b"secret_key_11111"


# generate random key and iv
def generate_key():
    global IV
    IV = Random.new().read(BLOCK_SIZE)
    global KEY
    KEY = Random.new().read(BLOCK_SIZE)


def add_padding(message):
    message_len = len(message)
    padding_len = BLOCK_SIZE - (message_len % BLOCK_SIZE)
    last_byte = padding_len.to_bytes(1, 'big')
    result = message + bytes([0] * (padding_len - 1)) + last_byte
    return result


def encrypt(plaintext):
    data = plaintext.encode()
    mac = hmac.new(KEY, data, hashlib.sha256).digest()
    message = data + mac
    padded_message = add_padding(message)
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    return aes.encrypt(padded_message)


def decrypt(ciphertext, p=False):
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


def guess_last_block_byte(fill_length, block_to_guess, byte_in_block_to_guess):
    while True:
        # generate new key and IV:
        generate_key()

        # Create encrypted message
        message = "A" * (BLOCK_SIZE + byte_in_block_to_guess) + "#" * fill_length + COOKIE + "B" * (
                BLOCK_SIZE - byte_in_block_to_guess)
        # print(message)
        encrypted_message = encrypt(message)
        hexed_encrypted_message = binascii.hexlify(encrypted_message)
        encrypted_message_blocks = [hexed_encrypted_message[i:i + 32] for i in
                                    range(0, len(hexed_encrypted_message), 32)]

        # Substitute the last block (the padding block) with the block we want to decrypt
        encrypted_message_blocks[-1] = encrypted_message_blocks[block_to_guess]

        # Check if the last byte of the substituted block makes a correct padding:
        cipher = binascii.unhexlify(b''.join(encrypted_message_blocks).decode())
        plain = decrypt(cipher)

        # If the padding is correct (the last byte of the deciphered block is 15 = 0f)
        if plain != 0:
            # Get the last byte of the last block of mac - block before the one that we are deciphering
            last_mac_block = encrypted_message_blocks[-2]
            # Get the block before the secret block
            first_block = encrypted_message_blocks[block_to_guess - 1]
            # Get the deciphered last byte
            deciphered_byte = chr(int("0f", 16) ^ int(last_mac_block[-2:], 16) ^ int(first_block[-2:], 16))
            return deciphered_byte


def poodle_attack():
    guessed_message = ''

    # getting the lengths of the 'A' and 'B' part
    ciphertext = binascii.hexlify(encrypt(COOKIE))
    original_length = len(ciphertext)
    fill_length = 1
    while True:
        length = len(binascii.hexlify(encrypt("A" * fill_length + COOKIE)))
        if length > original_length:
            break
        fill_length += 1

    # Modify block_to_guess and byte_in_block_to_guess in loop
    for block in range(original_length // 32 - 2, 0, -1):
        for i in range(BLOCK_SIZE):
            deciphered_byte = guess_last_block_byte(fill_length, block_to_guess=block, byte_in_block_to_guess=i)
            guessed_message = deciphered_byte + guessed_message

    # Removing the filler symbols from the beginning of the deciphered message
    guessed_message = re.sub(r"^\W+", "", guessed_message)
    print("Deciphered block: ", guessed_message)


poodle_attack()
