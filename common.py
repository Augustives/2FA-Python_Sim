import base64
import json

from backports.pbkdf2 import pbkdf2_hmac
from Crypto.Cipher import AES
from hashlib import sha256 as hash


def generate_salt(username, password):
    return base64.b32encode(
        username.encode('utf-8') +
        password.encode('utf-8')
    )


def compose_auth_token(username, password):
    salt = generate_salt(username, password)
    return pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        1000,
        32
    )


def compose_session_key(username, tfa_code):
    salt = generate_salt(username, tfa_code)
    return pbkdf2_hmac(
        'sha256',
        tfa_code.encode('utf-8'),
        salt,
        1000,
        32
    )


def scrypt(username, auth_token):    
    user_hash = hash()
    user_hash.update(
        username.encode("utf-8") +
        auth_token
    )

    return user_hash.hexdigest()


def encrypt_message(session_key, message):
    header = b"header"

    cipher = AES.new(session_key, AES.MODE_GCM)
    cipher.update(header)

    bytes_message = message.encode('utf-8')
    ciphertext, tag = cipher.encrypt_and_digest(bytes_message)

    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = [base64.b64encode(x).decode('utf-8') for x in [cipher.nonce, header, ciphertext, tag]]
    encrypted_message = json.dumps(dict(zip(json_k, json_v)))

    return encrypted_message


def decrypt_message(session_key, message):
    try:
        b64 = json.loads(message)

        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: base64.b64decode(b64[k]) for k in json_k}

        cipher = AES.new(session_key, AES.MODE_GCM, nonce=jv['nonce'])
        cipher.update(jv['header'])

        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])

        return plaintext
    except (ValueError, KeyError):
        raise ValueError("Error during decryption")
