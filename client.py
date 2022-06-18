from common import compose_auth_token


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