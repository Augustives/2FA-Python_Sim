from common import compose_auth_token, compose_session_key, encrypt_message, decrypt_message


class Client:
    def __init__(self):
        pass

    def login_register(self):
        username = input('Please write the username: \n')
        password =  input('Please write the password: \n')

        return (
            username, 
            compose_auth_token(
                username,
                password
            )
        )

    def two_factor_auth(self):
        qrcode_value = input('Please write QRCODE value: \n')
        return qrcode_value

    def get_encrypted_message_to_send(self, username, qrcode_value):
        session_key = compose_session_key(username, qrcode_value)

        message = input("\nPlease write the message: \n")
        encrypted_message = encrypt_message(session_key, message)

        return encrypted_message

    def receive_message_from_server(self, username, qrcode_value, message):
        session_key = compose_session_key(username, qrcode_value)

        decrypted_message = decrypt_message(session_key, message)

        return decrypted_message
