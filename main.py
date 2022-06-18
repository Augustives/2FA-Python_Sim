from sys import exit

from client import Client
from server import Server


CLIENT = Client()
SERVER = Server()


def login():
    print('----------------------------------------------------')
    print('### DOING LOGIN ###')
    username, auth_token = CLIENT.login_register()
    if not SERVER.login(username, auth_token):
        print('Incorret username/password or user not registered\n')
        return
    print('Logged in successfully')
    return two_factor_auth(username, auth_token)


def register():
    print('----------------------------------------------------')
    print('### REGISTERING USER ###')
    username, auth_token = CLIENT.login_register()
    if not SERVER.register_user(username, auth_token):
        return print('Failed to register user\n')
    print('Registered successfully')


def two_factor_auth(username, auth_token):
    print('----------------------------------------------------')
    print('### DOING 2FA ###')
    SERVER.two_factor_auth(username, auth_token)
    qrcode_value = CLIENT.two_factor_auth()
    if SERVER.validate_qrcode_value(qrcode_value):
        print('2FA successfully')
        return message_trading()
    else:
        print('Failed 2FA, try again')
        return two_factor_auth(username, auth_token)


def message_trading():
    print('----------------------------------------------------')
    print('### TRADING MESSAGES ###')


def user_action_dispatch():
    dispatch = {
        '1': login,
        '2': register,
        '3': exit
    }

    option = input(
        '\n### CHOOSE ONE OF THE FOLLOWING OPTIONS ###\n'
        '-Press 1 to login\n'
        '-Press 2 to register a new user\n'
        '-Press 3 to exit\n'
    )

    action = dispatch.get(option)
    if action:
        return action()


if __name__ == '__main__':
    running = True
    while running:
        user_action_dispatch()
