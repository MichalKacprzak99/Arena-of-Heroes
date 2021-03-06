import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # if you wanna play online uncomment 28 line and comment 29
        # self.server = '178.79.168.132'
        self.server = '127.0.0.1'
        self.port = 556
        self.adr = (self.server, self.port)
        self.p = self.connect()

    def get_player_id(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.adr)
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
