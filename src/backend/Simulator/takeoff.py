#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)

Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.

Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

### pi_test
from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, sys, argparse, math
#import take_cam

connection_string       = '/dev/ttyAMA0'

# Parse connection argument
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--connect", help="connection string")
parser.add_argument("--newlocation", help="new location")
args = parser.parse_args()

if args.connect:
   connection_string = args.connect

# Connect to the Vehicle
print ("Connecting")
vehicle = connect(connection_string,baud = 57600 ,wait_ready=True)

### Sitl
"""
# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None



# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()



# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
"""
### high
Alt = 10

def get_location_offset_meters(original_location, dNorth, dEast, alt):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the
    specified `original_location`. The returned Location adds the entered `alt` value to the altitude of the `original_location`.
    The function is useful when you want to move the vehicle around specifying locations relative to
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt+alt)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def get_5f(lator_lon):
    lator_lon=int(lator_lon*10000)/10000.0
    return lator_lon

###whether_fix_Alt
T_or_F_fix_Alt = 0

def fix_Alt_high(Alt,lat,lon):
    print("******fix_Alt_high******")
    global T_or_F_fix_Alt 
    T_or_F_fix_Alt = 1
    print("fix T_or_F_fix_Alt",T_or_F_fix_Alt)
    find = LocationGlobalRelative(lat, lon, Alt)
    vehicle.simple_goto(find)
    while True:
        print(" Alt: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= Alt * 0.95:
            print("Reached target altitude to find")
            print("going take_pic")
            break
        #time.sleep(1)
        
def reach_place(point,lat,lon):
    while True:
        #lat = str(vehicle.location.global_frame.lat)
        #lon = str(vehicle.location.global_frame.lon)
        #print(point,"lat: ",(format(vehicle.location.global_frame.lat,'.5f')))
        #print(point,"lon: ",(format(vehicle.location.global_frame.lon,'.5f')))
        #print(point,"lat: ",int(vehicle.location.global_frame.lat*10000)/10000.0)
        #print(point,"lon: ",int(vehicle.location.global_frame.lon*10000)/10000.0)
        # roll，pitch，yaw，rad，-n to n）
        #print(point,"Attitude: %s" % vehicle.attitude)
        # 0 ~ 360
        #print(point,"Heading: %s" % vehicle.heading)
        
        if((get_5f(vehicle.location.global_frame.lat)==get_5f(lat)) and (get_5f(vehicle.location.global_frame.lon)==get_5f(lon))):
            print("Reach place")
            time.sleep(2)
            break

temp_input = sys.argv
new_location = temp_input[4].split(',')
print("new_location lat : ",new_location[0])
print("new_location lon : ",new_location[1])


home = vehicle.location.global_relative_frame
arm_and_takeoff(Alt)

print("Set default/target airspeed to 3")
vehicle.airspeed = 7

#Global Location lat: 22.7370774
#Global Location lon: 121.0665216

#### point1
print("******** Going point1 ******** ")
wp = LocationGlobalRelative(float(new_location[0]), float(new_location[1]), Alt)
vehicle.simple_goto(wp)
time.sleep(3)
print("Alt",Alt)
reach_place(wp, wp.lat, wp.lon)
time.sleep(10)

#### RTL
print("******** Returning to Launch ********")
vehicle.mode = VehicleMode("RTL")
time.sleep(3)

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()


"""
#### point1
print("******** Going  point1 ******** ")
#point1 = LocationGlobalRelative(22.736709,  121.066511,20 )
point1 = LocationGlobalRelative(22.737259,  121.066681,Alt )
vehicle.simple_goto(point1)

# sleep so we can see the change in map
#time.sleep(30)
point="point1 : "
#reach_place(point,point1.lat,point1.lon)
print("T_or_F_fix_Alt",T_or_F_fix_Alt)
print("Alt",Alt)

#if(T_or_F_fix_Alt == 1):
#### point2
print("******** Going point2  (groundspeed set to 10 m/s) ... ********")
point2 = LocationGlobalRelative(22.737238, 121.066565, Alt)
vehicle.simple_goto(point2)

# sleep so we can see the change in map
#time.sleep(30)
point="point2 : "
#reach_place(point,point2.lat,point2.lon)

#### point3
print("******** Going point3 ********")
point3 = LocationGlobalRelative(22.737214, 121.066474,Alt)
vehicle.simple_goto(point3)

# sleep so we can see the change in map
#time.sleep(30)
point="point3 : "
#reach_place(point,point3.lat,point3.lon)

#### point4
print("******** Going point4 ********")
point4 = LocationGlobalRelative(22.737145, 121.066468,Alt)
vehicle.simple_goto(point4)

# sleep so we can see the change in map
#time.sleep(30)
point="point4 : "
#reach_place(point,point4.lat,point4.lon)

#### point5
print("******** Going point5 ********")
point5 = LocationGlobalRelative(22.737145, 121.066550,Alt)
vehicle.simple_goto(point5)

# sleep so we can see the change in map
#time.sleep(30)
point="point5 : "
#reach_place(point,point5.lat,point5.lon)

print("******** Returning to Launch ********")
vehicle.mode = VehicleMode("RTL")


# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
"""

"""
#### point6
print("******** Going point6 ********")
point6 = LocationGlobalRelative(22.737142, 121.066635,Alt)
vehicle.simple_goto(point6)

# sleep so we can see the change in map
#time.sleep(30)
point="point6 : "
reach_place(point,point6.lat,point6.lon)
"""
"""
#### point7
print("******** Going point4 ********")
point7 = LocationGlobalRelative(22.737050, 121.066592,Alt)
vehicle.simple_goto(point7)

# sleep so we can see the change in map
#time.sleep(30)
point="point7 : "
reach_place(point,point7.lat,point7.lon)


#### point8
print("******** Going point8 ********")
point8 = LocationGlobalRelative(22.737067, 121.066477,Alt)
vehicle.simple_goto(point8)

# sleep so we can see the change in map
#time.sleep(30)
point="point8 : "
reach_place(point,point8.lat,point8.lon)

#### point9
print("******** Going point9 ********")
point9 = LocationGlobalRelative(22.737067, 121.066477,Alt)
vehicle.simple_goto(point9)
time.sleep(5)
# sleep so we can see the change in map
#time.sleep(30)
point="point9 : "
reach_place(point,point9.lat,point9.lon)
"""


"""
print("******** Returning to Launch ********")
vehicle.mode = VehicleMode("RTL")


print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")


# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
"""

"""
# Shut down simulator if it was started.
if sitl:
    sitl.stop()
"""

