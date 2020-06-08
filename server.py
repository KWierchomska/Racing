import socket
from _thread import *
import pickle
import car_customization
import base64

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# listen for two Clients
s.listen(2)
print("Waiting for a connection, Server Started")

player1 = {'x': 320,
           'y': 270,
           'color': car_customization.cars[0],
           "dir": 0,
           "speed": 0.0,
           "max_speed": 20,
           "min_speed": -5,
           "acceleration": 0.2,
           "deacceleration": 2,
           "softening": 0.04,
           "steering": 1.6,
           "tracks": False}
player2 = {'x': 320,
           'y': 270,
           'color': car_customization.cars[1],
           "dir": 0,
           "speed": 0.0,
           "max_speed": 20,
           "min_speed": -5,
           "acceleration": 0.2,
           "deacceleration": 2,
           "softening": 0.04,
           "steering": 1.6,
           "tracks": False}

players = [player1, player2]
flags = [False, False]


def threaded_client(conn):
    conn.send(base64.b64encode(pickle.dumps(players)))
    while True:
        try:
            conn.send(base64.b64encode(pickle.dumps(flags)))
            data = pickle.loads(base64.b64decode(conn.recv(2048 * 2 * 2)))
            players[0] = data[0]
            players[1] = data[1]
            if not data:
                print("Disconnected")
                break
        except socket.error as e:
            str(e)
            break

    print("Lost connection")
    conn.close()


def threaded_client2(conn):
    conn.send(base64.b64encode(pickle.dumps(players)))
    while True:
        try:
            conn.send(base64.b64encode(pickle.dumps(players)))
            data = pickle.loads(base64.b64decode(conn.recv(2048 * 2 * 2)))
            flags[0] = data[0]
            flags[1] = data[1]
        except socket.error as e:
            str(e)
            break

    print("Lost connection")
    conn.close()


def clients_handling():
    current_player = 0
    while True:
        conn, addr = s.accept()
        print("Connected to: ", addr)

        if current_player == 0:
            start_new_thread(threaded_client, (conn,))
            current_player += 1
        else:
            start_new_thread(threaded_client2, (conn,))


clients_handling()
