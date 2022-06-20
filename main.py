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
        return message_trading(username, qrcode_value)
    else:
        print('Failed 2FA, try again')
        return two_factor_auth(username, auth_token)


def message_trading(username, qrcode_value):
    print('----------------------------------------------------')
    print('### TRADING MESSAGES ###')

    options = {
        "1": "send_message",
        "2": "return"
    }

    user_option = input(
        '\n### CHOOSE ONE OF THE FOLLOWING OPTIONS ###\n'
        '-Press 1 to send a message\n'
        '-Press 2 to go back\n'
    )

    while options[user_option] == "send_message":
        message = CLIENT.get_encrypted_message_to_send(username, qrcode_value)
        print(f"\nEncrypted message sent from client to server: {message}")

        response_message_encrypted = SERVER.receive_and_return_new_message(username, qrcode_value, message)
        print(f"Encrypted message sent from server to client: {response_message_encrypted}")

        response_message = CLIENT.receive_message_from_server(username, qrcode_value, response_message_encrypted)

        print("\n### MESSAGE RECEIVED FROM SERVER ###")
        print(response_message.decode("utf-8"))

        user_option = input(
            '\n### CHOOSE ONE OF THE FOLLOWING OPTIONS ###\n'
            '-Press 1 to send another message\n'
            '-Press 2 to go back\n'
        )

    return


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
