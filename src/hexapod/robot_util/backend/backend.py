import base64
from socketIO_client import SocketIO, LoggingNamespace
import threading

class BackEnd(object):

    def __init__(self):
        self.socketIO = SocketIO('http://192.168.0.170', 8080, LoggingNamespace)
        self.__robot = {
            'type': "GR",
            'ID': 2,
            'position_GPS': {
                'lat': -1,
                'lng': -1
            },
            'position_bluetooth': {
                'x':1,
                'y':2
            },
            'host':'192.168.0.168:8081',
            'rgb':'GR2_rgb.jpg',
            'red':'GR2_red.jpg'
        }
        self.__stop = 0
        self.control = []
        
        self.__connect()

    def __update_location(self):
        point = {
            "x": -1,
            "y": -1
        }
        self.__robot['position_bluetooth']['x'] = point['x']
        self.__robot['position_bluetooth']['y'] = point['y']
        self.socketIO.emit('update_location', {'robot': self.__robot, 'command': 'update location'+'UAV1'})
        if self.__stop == 0:
            t = threading.Timer(1.0, self.__update_location)
            t.start()

    def move(self, data):
        if data['robot']['type'] == self.__robot['type'] and data['robot']['ID'] == self.__robot['ID']:
            self.control.append(data['Move_command'])


    def __keep_alive(data, self):
        self.socketIO.emit('new_robot', self.__robot)
        self.socketIO.emit('ack', {'robot' : self.__robot, 'command' : 'keep_alive', 'state' : 'OK'})

    def __back_recv(self):
        global t
        self.socketIO.emit('new_robot', self.__robot)
        self.t.start()
        self.socketIO.on('keep_alive', self.__keep_alive())
        self.socketIO.on('move', self.move)
        self.socketIO.wait()

    def get_rgb_image(self):
        with open('../dpu/rgb.jpg', 'rb') as f:
            image_data = base64.b64encode(f.read()).decode("ascii")
        self.socketIO.emit('get_rgb_image', {'robot': self.__robot, 'image_data': image_data})

    def get_red_image(self):
        with open('rgb.jpg', 'rb') as f:
            image_data = base64.b64encode(f.read()).decode("ascii")
        self.socketIO.emit('get_red_image', {'robot': self.__robot, 'image_data': image_data})

    def response(self):
        self.socketIO.emit('find', {'robot':self.__robot})

    def __connect(self):
        self.t = threading.Timer(5.0, self.__update_location())
        sio = threading.Thread(target = self.__back_recv())
        sio.start()


