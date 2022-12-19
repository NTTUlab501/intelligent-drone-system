import socket
import json

class Connect(object):

    def __init__(self, host, port):
        self.__serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__serversocket.bind((host, port))
        self.__serversocket.listen(1)
        

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.__robotsocket.send(bytes(json_data, encoding="utf-8"))
            
    def reliable_recv(self):
        json_data = bytearray(0)
        while True:
            try:
                json_data += self.__robotsocket.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue

    def connect(self):
        print("waiting for connection...")
        self.__robotsocket, self.__ip = self.__serversocket.accept()
        print(f"\033[1;32;1m{self.__ip} is connect\033[0m")
