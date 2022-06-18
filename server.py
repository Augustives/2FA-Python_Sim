import pyotp
import qrcode
import io

from common import scrypt, generate_salt


class Server:
    def __init__(self):
        self.users = {
            '123': '10b8086be548ff7f074edf0266637f4f87bc013298a18ca376bf943d274a71fb'
        }
        self.user_logged = None

    def login(self, username, auth_token):
        stored_user_hash = self.users.get(username) or {}
        login_user_hash = scrypt(
            username,
            auth_token
        )

        if stored_user_hash != login_user_hash:
            return False

        self.logged_user = username
        return True

    def register_user(self, username, auth_token):
        if self.users.get(username):
            return False

        self.users[username] = scrypt(
            username,
            auth_token
        )

        return True

    def two_factor_auth(self, username, auth_token):
        self.totp = pyotp.TOTP(generate_salt(
            username,
            str(auth_token)
        ))
        
        qrcode_obj = qrcode.QRCode()
        qrcode_obj.add_data(self.totp.now())
        self.print_qrcode(qrcode_obj)

    def print_qrcode(self, qrcode_obj):
        f = io.StringIO()
        qrcode_obj.print_ascii(out=f)
        f.seek(0)
        print(f.read())

    def validate_qrcode_value(self, qrcode_value):
        return self.totp.verify(qrcode_value)
