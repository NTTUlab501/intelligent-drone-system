# -*- coding:utf-8 -*-

import cv2
import numpy as np
from flask import  request, render_template, redirect, jsonify, send_file, Response
from . import user_access
from .. import socketio, bootstrap
from . import robots
import json
from time import sleep

'''
@user_access.route('/color')
def color():
    return render_template('color.html')
'''

@user_access.route('/', methods = ['GET'])
def index():
    global  robots
    print(robots)
    
    current_robot = request.args.get('current_robot')
    return render_template('index.html', current_robot = current_robot, robots=robots)

@user_access.route('/robot/<string:robot_type>/<int:id>/<string:host>', methods = ['GET'])
def show_robot(robot_type, id,host):
    return render_template('robot.html', robots=robots, robot_type=robot_type, id=id, host=host)

@user_access.route('/map')
def map():
    return render_template('map.html')

@user_access.route('/home6')
def home6():
    return render_template('home6.html')


@user_access.route("/status", methods=['GET'])
def upload():
    socketio.emit('status_response', {'data': 123})
    
    return jsonify(
        {"response": "ok"}
    )

@user_access.route("/showstatus")
def home():
    return render_template('sockettest.html')

@user_access.route('rgb/<string:rgb>/<int:time>')
def rgb(rgb, time):
    filename = 'User_Access/static/images/' + rgb
    return send_file(filename, mimetype='image/jpg')

'''
@user_access.route('red/<string:red>/<int:time>')
def red(red, time):
    filename = 'User_Access/static/images/' + red
    return send_file(filename, mimetype='image/jpg')
'''
'''
def gen_frames():
    while True:
        img = cv2.imread('/home/bryan/backend/app/User_Access/static/images/UAV1_rgb.jpg')
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        sleep(0.5)
'''

def gen_frames():
    while True:
        frame  = open('/home/bryan/backend/app/User_Access/static/images/UAV1_rgb.jpg', 'rb').read()
        frame = frame.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #sleep(0.5)

@user_access.route('video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

