import socket
import random
import time

def start_client():
    '''
    function generate a random coordinate and send to server and wait answer
    :return: None
    '''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)
    print("Connected to the server at {}:{}".format(*server_address))

    try:
        while True:
            # Generate client coordinates
            client_coordinates = (random.uniform(0, 10), random.uniform(0, 10))

            # Send coordinates to the server
            message = "{},{}".format(*client_coordinates)
            client_socket.sendall(message.encode('utf-8'))

            # Receive and print the server's response
            response = client_socket.recv(1024).decode('utf-8')
            print(response)

            time.sleep(1)

    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
