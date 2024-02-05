import socket
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import ticker

size_of_obstacles = 1  # size of obstacle in metres
def start_server():
    '''
    create a server
    :return: None
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Server is listening on {}:{}".format(*server_address))

    #Create a map with obstacles
    n = 5 #count of obstacles
    x_max = 10 #max of length of x-axe
    y_max = 10 #max of length of y-axe
    list_coords = []
    fig, ax = plt.subplots()
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    for _ in range(n):
        obstacle_position = (random.randint(0, 9), random.randint(0, 9))
        list_coords.append(obstacle_position)
        obstacle_patch = patches.Rectangle(obstacle_position, size_of_obstacles, size_of_obstacles, edgecolor='None', facecolor='red')
        ax.add_patch(obstacle_patch)

    client_marker, = ax.plot([], [], 'bo', label='Client')
    maj_pos = ticker.MultipleLocator(1)
    min_pos = ticker.MultipleLocator(1)
    ax.xaxis.set(major_locator=maj_pos, minor_locator=min_pos)
    ax.yaxis.set(major_locator=maj_pos, minor_locator=min_pos)
    plt.grid()

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connected to {}".format(client_address))

        try:
            while True:
                # Receive client coordinates
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                client_coordinates = tuple(map(float, data.split(',')))

                # Check for intersection with the obstacle
                if intersects(client_coordinates, list_coords):
                    response = "Intersection with obstacle"
                else:
                    response = "No intersection with obstacle"

                # Update client marker position
                client_marker.set_xdata(client_coordinates[0])
                client_marker.set_ydata(client_coordinates[1])

                # Send the response back to the client
                client_socket.sendall(response.encode('utf-8'))

                # Update the plot
                plt.draw()
                plt.pause(0.1)

        finally:
            client_socket.close()

def check_coordinate(min_coordinate, current_coordinate):
    max_coordinate = min_coordinate + size_of_obstacles
    if min_coordinate < current_coordinate < max_coordinate:
        return True
    return False
def intersects(client, list_coords):
    '''
    function for check an intersection between client and obstacle
    :param client: coordinates of client
    :param list_coords: coordinates of all obstacles
    :return: True or False
    '''
    for coordinate in list_coords:
        if check_coordinate(coordinate[0], client[0]) and check_coordinate(coordinate[1], client[1]):
            return True
    return False

if __name__ == "__main__":
    start_server()
