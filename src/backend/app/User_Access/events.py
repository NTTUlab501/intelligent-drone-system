# -*- coding:utf-8 -*-

import cv2
from flask import session
from flask_socketio import emit
from . import robots
from .. import socketio
from threading import Lock
import json
import numpy as np
import base64

thread = None
thread_lock = Lock()

@socketio.on('connect')
def connect():
    socketio.emit('update',robots)
    print('connect')

@socketio.on('disconnect')
def disconnect():
    global robots
    robots = {'UAV': []}
    socketio.emit('update',robots)
    socketio.emit('keep_alive')
    
    #print(robots)
    print('Client disconnected')
    

@socketio.on('new_robot')
def new_robot(robot_info):
    global robots
    
    if robot_info is not None:
        if robot_info['type'] == 'UAV' and robot_info not in robots['UAV']:
            robots['UAV'].append(robot_info)

        socketio.emit('update',robots)
        print("=======================")
        print(robots)

@socketio.on('ack')
def ack(msg):
    print(msg)

@socketio.on('user_control')
def user_control(data):
    print(data)
    socketio.emit('move', {'robot': data['robot'], 'Move_command': data['Move_command']})
    #socketio.emit('test', { 'Move_command': robot['Move_command'] }, namespace = '/test')

@socketio.on('connect', namespace='/test')
def test():
    print('namespace is connect')
    socketio.emit('test', 'this is test.', namespace='/test')
    print('is emit')

@socketio.on('plan')
def handleplan(position):
    global robots
    UAV_cnt = len(robots['UAV'])
    if UAV_cnt <= 0:
        result = {
            'state': 'fail',
            'message': 'No UAV connect.',
            'plan': []
        }
    else:
        scopes = []
        paths = []
        for i in range(1, 10):
            if len(robots['UAV']) <= i ** 2:
                scope_cnt = i 
                break

        scope_left_low = {
            'lat': position['lat'] - 1 / 111 / 2,
            'lng': position['lng'] - 0.01 / 2
        }
        mash_unit = {
            'lat': 1 / 111 / scope_cnt,
            'lng': 0.01 / scope_cnt
        }
        for i in range(scope_cnt):
            for j in range(scope_cnt):
                scope = [
                    {'lat': scope_left_low['lat'] + mash_unit['lat'] * i, 'lng': scope_left_low['lng'] + mash_unit['lng'] * j},
                    {'lat': scope_left_low['lat'] + mash_unit['lat'] * (i + 1), 'lng': scope_left_low['lng'] + mash_unit['lng'] * j},
                    {'lat': scope_left_low['lat'] + mash_unit['lat'] * (i + 1), 'lng': scope_left_low['lng'] + mash_unit['lng'] * (j + 1)},
                    {'lat': scope_left_low['lat'] + mash_unit['lat'] * i, 'lng': scope_left_low['lng'] + mash_unit['lng'] * (j + 1)}
                ]
                scopes.append(scope)

                path = []
                now_pos = {'lat': scope[0]['lat'] + 1 / 111 / 20, 'lng': scope[0]['lng'] + 0.01 / 20}
                op = 1
                while now_pos['lat'] < scope[1]['lat']:
                    while now_pos['lng'] > scope[0]['lng'] and now_pos['lng'] < scope[3]['lng']:
                        new_pos = now_pos.copy()
                        path.append(new_pos)
                        now_pos['lng'] += 0.01 / 20 * op
                        print('in')
                    now_pos['lng'] -= 0.01 / 20 * op 
                    now_pos['lat'] += 1 / 111 / 20
                    op *= -1
                    print('out')
                paths.append(path)

        #print(paths) 


        
        result = {
            'state': 'OK',
            'message': 'complete',
            'scopes': scopes,
            'paths': paths
        }

        #print(result)
    socketio.emit('plan_update', result)

@socketio.on('update_location')
def update_location(data):
    global robots

    robot = data['robot']
    if robot['type'] == 'UAV':
        for i in range(len(robots['UAV'])):
            if robots['UAV'][i]['ID'] == robot['ID']:
                robots['UAV'][i]['position_GPS'] = robot['position_GPS']
                robots['UAV'][i]['AQI_pms'] = robot['AQI_pms']
                robots['UAV'][i]['AQI_dpu'] = robot['AQI_dpu']
                break
    # print('robot : ')
    # print(robot)
    # print('=================================robots : =======================================')
    # print(robots)
    socketio.emit('update',robots)


@socketio.on('get_rgb_image')
def get_rgb_image(data):
    global robots

    robot = data['robot']

    with open('app/User_Access/static/images/' + robot['rgb'], "wb") as img:
        img.write(base64.b64decode(data['image_data']))
        #print (data['image_data'])

@socketio.on('get_yolo_image')
def get_rgb_image(data):
    global robots

    robot = data['robot']
    with open('app/User_Access/static/images/' + robot['yolo'], "wb") as img:
        img.write(base64.b64decode(data['image_data']))

"""
@socketio.on('get_red_image')
def get_rgb_image(data):
    global robots

    robot = data['robot']
    with open('app/User_Access/static/images/' + robot['red'], "wb") as img:
        img.write(base64.b64decode(data['image_data']))
"""

@socketio.on('get_taget_position_input')
def get_taget_position_input(data):
    print(":::::::::get target position : ")
    print(data)
    print(type(data))
    socketio.emit('get_taget_position', data)

@socketio.on('get_taget_scope_input')
def get_taget_scpoe_input(data):
    print(data)
    socketio.emit('get_taget_scope', data)

@socketio.on('uav_find')
def uav_find(data):
    print("**************")
    print(data)
    socketio.emit('get_uav_find', data)
    
@socketio.on('pms_detect')
def pms_detect(data):
    print("**************")
    print(data)
    socketio.emit('get_pms_detect', data)

@socketio.on('dpu_detect')
def dpu_detect(data):
    # print("*******DPU_AQI*******")
    robot = data['robot']
    #　print(robot)
    socketio.emit('get_dpu_detect', robot)