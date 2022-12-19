from robot_util.connect import Connect

class RaspberryPi(object):

    def __init__(self, socket_host, socket_port):
        self.__connect = Connect(socket_host, socket_port)

    def connect(self):
        self.__connect.connect()

    def send_command(self, data):
        self.__connect.reliable_send(data)
        return self.__connect.reliable_recv()
           
    def take_thermal_photo(self):
        return self.__connect.send_command("take_thermal_photo")
