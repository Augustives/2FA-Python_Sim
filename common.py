import base64

from backports.pbkdf2 import pbkdf2_hmac
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


def scrypt(username, auth_token):    
    user_hash = hash()
    user_hash.update(
        username.encode("utf-8") +
        auth_token
    )

    return user_hash.hexdigest()
