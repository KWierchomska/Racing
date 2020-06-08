import socket
import pickle
import base64


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.players = self.connect()

    def get_players(self):
        return self.players

    def connect(self):
        try:
            print("Connecting...")
            self.client.connect(self.addr)
            return pickle.loads(base64.b64decode(self.client.recv(2048 * 2)))
        except socket.error as e:
            str(e)

    def send(self, data):
        try:
            self.client.send(base64.b64encode(pickle.dumps(data)))
        except socket.error as e:
            print(e)

    def send_flags(self, data):
        try:
            self.client.send(base64.b64encode(pickle.dumps(data)))
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return pickle.loads(base64.b64decode(self.client.recv(2048 * 2 * 2)))
        except socket.error as e:
            print(e)

    def receive_flags(self):
        try:
            return pickle.loads(base64.b64decode(self.client.recv(2048 * 2 * 2)))
        except socket.error as e:
            print(e)
