import socketio

robot = {
    'type': "UAV",
    'ID': '1',
    'position_GPS': {
        'lat': 22.7365759,
        'lng': 121.0657083
    }
}


#sio = socketio.Client(logger=True, engineio_logger=True)
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print("I'm connected to the /chat namespace!")

@sio.on('move', namespace=robot['type'] + robot['ID'])
def handletest(msg):
    print(msg)

def keep_alive():
    global sio
    global robot
    sio.emit('new_robot',robot)
    sio.emit('ack', {'robot' : robot, 'command' : 'keep_alive', 'state' : 'OK'})

def move(ins):
    print(ins)
try:
    sio.connect('http://localhost:8080')
    sio.wait()
except:
    sio.disconnect()