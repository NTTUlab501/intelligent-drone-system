from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import json
import os
import threading
import time

socketIO = SocketIO('http://192.168.0.105', 8080, LoggingNamespace)

robot = {
    'type': "GR",
    'ID': 1,
    'position_GPS': {
        'lat': 22.7365759,
        'lng': 121.0657083
    },
    'position_bluetooth': {
        'x':5,
        'y':5
    },
    'host':'127.0.0.1:8081'
    
}

def keep_alive():
    global socketIO
    global robot
    socketIO.emit('new_robot',robot)
    socketIO.emit('ack', {'robot' : robot, 'command' : 'keep_alive', 'state' : 'OK'})

def move(ins):
    print(ins)
stop = 0
op = 1
def update_location():
    global socketIO
    global t
    global robot
    global op
    global stop
    robot['position_bluetooth']['x'] += op
    op *= -1
    socketIO.emit('update_location', {'robot': robot, 'command': 'update location'+'UAV1'})
    print('test')
    if stop == 0:
        t = threading.Timer(1.0, update_location)
        t.start()


try:
    socketIO.emit('new_robot', robot)
    t = threading.Timer(5.0, update_location)
    t.start()
    socketIO.on('keep_alive',keep_alive)
    socketIO.on('move',move)
    socketIO.wait()
except KeyboardInterrupt:
    stop = 1
    t.join()
  


'''
def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def on_aaa_response(*args):
    print('on_aaa_response', args)

# Listen
socketIO.on('aaa_response', on_aaa_response)
socketIO.emit('aaa')
socketIO.emit('aaa')
socketIO.wait(seconds=1)

# Stop listening
socketIO.off('aaa_response')
socketIO.emit('aaa')
socketIO.wait(seconds=1)

# Listen only once
socketIO.once('aaa_response', on_aaa_response)
socketIO.emit('aaa')  # Activate aaa_response
socketIO.emit('aaa')  # Ignore
socketIO.wait(seconds=1)
'''
