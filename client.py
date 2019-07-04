import errno
import socket
import sys


# default values
HEADER_LENGTH = 10
IP = '10.68.100.126'
PORT = 1234

# user enters a username when joining the chat
my_username = input('Input a username: ')

# connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# send username information through to the server so it can process your messages
username = my_username.encode('utf-8')
username_header = f'{len(username):<{HEADER_LENGTH}}'.encode('utf-8')
client_socket.send(username_header + username)

# never stop running whilst the program is active
while True:
    message = input(f'{my_username} >>> ')

    # check that what the user typed and tries to send contains characters
    if message:
        message = message.encode('utf-8')
        message_header = f'{len(message):<{HEADER_LENGTH}}'.encode('utf-8')
        client_socket.send(message_header + message)

    # send the message to the server ready to be broadcast to the other users currently online
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)

            # if someone tries to spoof a message exit the program
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # send username to the server
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            # send message to the server
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # print locally what the user sent
            print(f'{username} > {message}')

    # if we find these two errors, exit the program
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: ', str(e))
            sys.exit()

        continue

    # a general error occurred, exit the program
    except Exception as e:
        print('General error: ', str(e))
        sys.exit()
