import socket
from _thread import *
import pickle
import car_customization
import pygame_classes


server = '192.168.1.104' #"192.168.43.250"  # your IPv4 Address - to get it write in console 'ipconfig' -> Wireless LAN adapter Wi-Fi: -> IPv4 Address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# listen for two Clients
s.listen(2)
print("Waiting for a connection, Server Started")

player1 = { 'x': 350,
            'y': 250,
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
player2 = { 'x': 350,
            'y': 250,
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


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 2))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


def main():
    current_player = 0
    while True:
        conn, addr = s.accept()
        print("Connected to: ", addr)

        start_new_thread(threaded_client, (conn, current_player))
        current_player += 1


main()