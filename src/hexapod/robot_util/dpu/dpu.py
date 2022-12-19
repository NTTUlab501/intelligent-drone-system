from robot_util.connect import Connect
import base64
import robot_util.connect
from robot_util.web_cam import WebCam


class DPU(object):
    def __init__(self):
        #self.__connect = Connect("192.168.2.99", 12345)
        self.__webcam = WebCam()

        #self.__connect.connect()

    def take_photo(self):
        self.__webcam.take_photo()

    def detect(self):
        self.take_photo()

        with open('rgb.jpg', 'rb') as f:
            self.__connect.reliable_send(base64.b64encode(f.read()).decode("ascii"))
        return self.__connect.reliable_recv()