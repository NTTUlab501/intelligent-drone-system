import base64
import cv2
import numpy as np
from socketIO_client import SocketIO, LoggingNamespace
import threading
from subprocess import Popen, PIPE, run
import subprocess
import os
from time import sleep
import random

# from robot_util.bluetooth import BluetoothMaster
# from robot_util.backend import BackEnd
# from robot_util.connect import Connect
# from robot_util.dpu import DPU
# from robot_util.raspberry_pi import RaspberryPi
from robot_util.robot import Robot

aqi = 1

class SpiderBot(Robot):

    def __init__(self, id, socket_host, socket_port, bluetooth_ip_bass_address=0,
                bluetooth_address_range=0, type="UAV"):
        print("initializing...")
        super().__init__(id, type)
        #self.__run_ActionGroup = run_ActionGroup
        self.__gps_position = None
        self.__stop = False
        self.__find = False
        self.__aqi = 0
        self.__pms = False
        self.__gps = None
        #self.pynqZ2 = RaspberryPi(socket_host, socket_port) # 接pynqZ2的時候打開
        print("connect backend...")
        self.__socketIO = SocketIO('http://192.168.10.18', 8080, LoggingNamespace)
        #self.__socketIO = SocketIO('http://219.70.21.40', 5000, LoggingNamespace)
        print("connect")
        # 玉山主峰： 23.470213305523, 120.95756197299595
        # 國立臺灣大學傅鐘： 25.017204654352824, 121.53676750209746
        self.__robot = {
            'type': "UAV",
            'ID': 1,
            'position_GPS': {
                'lat': 25.017204,
                'lng': 121.536767
            },
            'host':'192.168.10.18:8081',
            'rgb':'UAV1_rgb.jpg',
            'AQI_pms':'0',
            'AQI_dpu':aqi
        }
        self.__socketIO.emit('new_robot', self.__robot)
        self.__socketIO.on('get_taget_position', self.__get_taget_position)
        self.__socketIO.on('keep_alive', self.__keep_alive)
        #self.__socketIO.on('move', self.__move_control)
        print("\033[1;32;1mcomplete\033[0m")

    def __update_location(self):
        self.__socketIO.emit('update_location', {'robot': self.__robot, 'command': 'update location'+'UAV1'})
    
    def __repeat_update_location(self):
        while  not self.__stop:
            self.__update_location()
            sleep(0.01)

    def __get_taget_position(self, target_position):
        print(target_position)
        # 在這裡呼叫raspberrypi的飛控並給予目的座標

    def __move_control(self, data):
        print(f"[I] move control: command is {data['Move_command']}")
        if data['robot']['type'] == self.__robot['type'] and data['robot']['ID'] == self.__robot['ID']:
            self.__move(str(data['Move_command']), 1)
    
    def __keep_alive(self):
        print("[I] keep alive")
        self.__socketIO.emit('new_robot', self.__robot)
        
    def send_rgb_image(self, frame):
        #with open('rgb.jpg', 'rb') as f:
            #image_data = base64.b64encode(f.read()).decode("ascii")
        image_data = cv2.imencode('.jpg', frame)[1]
        image_data = base64.b64encode(image_data).decode()
        self.__socketIO.emit('get_rgb_image', {'robot': self.__robot, 'image_data': image_data})


    def response(self):
        self.__socketIO.emit('get_target', {'robot':self.__robot})

    def __move(self, direct, step):
        command = "move" + direct
        print(command)
        self.__run_ActionGroup(direct, step)
        # self.raspberry_pi.send_command(command)

    def get_bluetooth_position(self):
        pass

    def get_gps_position(self):
        pass

    ## DPU辨識
    def dpu_detect(self):
        while not self.__find and not self.__stop:
            #self.pynqZ2.send_command("detect")
            # "空氣辨識子程式在這"
            
            # fake aqi level
            '''
            sys_command = "python3 FakeOutput"
            print("end")
            ret = subprocess.run(
                sys_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("AQI Level ： ", ret.stdout.decode('utf-8'))
            # aqi = ret.stdout.decode('utf-8')
            '''
            
            aqi = random.randint(1,6)
            # print("aqi = " + str(aqi))
            
            # print("\n================" + self.__robot + "================\n")
            
            if  aqi != "0":
                self.__robot['AQI_dpu'] = aqi
                # print(self.__robot['AQI_dpu'])
                self.__socketIO.emit("dpu_detect", {'robot':self.__robot})
            sleep(1)
            
          
    def pms_detect(self):
        while not self.__pms:
            self.__socketIO.emit("pms_detect",self.__robot['type']+str(self.__robot['ID'])+str(self.__robot['AQI_pms']))
            sleep(0.5)

    def stream(self):
        print(123)
        video = cv2.VideoCapture(0)
        video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        print(456)
        #D = start() # 插熱像儀的時候打開

        if not video.isOpened():
            print("no camara")
            return None
        while not self.__stop:
            ret, frame = video.read()
            #D.Detect() # 插熱像儀的時候打開
            
            if ret:
                # print(ret)
                #if not self.__find:
                    #cv2.imwrite('images/rgb.jpg', frame)
                self.send_rgb_image(frame)
                #self.send_red_image()
            #print("[I] take picture")
            sleep(0.01)



    def start(self):
        try:
            threading.Thread(target=self.__repeat_update_location).start()
            threading.Thread(target=self.dpu_detect).start() # 影像辨識
            # threading.Thread(target=self.stream).start() # 串流
            # threading.Thread(target=self.pms_detect).start() # PMS detect
            self.__socketIO.wait()
        except KeyboardInterrupt:
            self.__stop = True

