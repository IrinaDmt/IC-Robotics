#!/usr/bin/python
from BrickPi import *
import math
from self_adjusting_utilities import *
import sys

SONAR = PORT_1
DESIRED_DISTANCE = 30 #cm
INIT_SPEED = 100
SENSOR_SAMPLE_COUNT = 5

# actual median function only available in python 3.3+
# this version is 2.7.3
def median(list):
	odd = len(list) % 2
	ordered = sorted(list)
	length = len(list)
	if odd:
		return ordered[length / 2]
	else:
		a = ordered[(length + 1) / 2]
		b = ordered[(length - 1) / 2]
		return (a + b) / 2

# --- start program ---

BrickPiSetup()
BrickPi.SensorType[SONAR] = TYPE_SENSOR_ULTRASONIC_CONT
BrickPiSetupSensors()
distance_measurements = []

while len (distance_measurements) < SENSOR_SAMPLE_COUNT: #should be odd if integer results are desired
	result = BrickPiUpdateValues()
	if not result:
		distance_measurements.insert(0, BrickPi.Sensor[SONAR])

def get_distance():
	global distance_measurements
	#calculate median distance over last 10 results
	distance_measurements.pop()
	distance_measurements.insert(0, BrickPi.Sensor[SONAR])
	distance = median(distance_measurements)
	#  print "all ", distance_measurements
	return distance

#initialise to medium speeds at the beggining of the program
BrickPi.MotorSpeed[PORT_A] = INIT_SPEED
BrickPi.MotorSpeed[PORT_B] = INIT_SPEED + 2

sum = 200

BASE_SPEED_LEFT = 100
BASE_SPEED_RIGHT = 102

def my_left(x):
	right(x)

def my_right(x):
	left(x)

def my_fwd(x):
	print "going fwd"
	BrickPi.MotorSpeed[PORT_A] = 100
	BrickPi.MotorSpeed[PORT_B] = 100
	timer(3)

def go_closer(dist):
	print "going closer"
	#go closer
	new_dist = dist
	ang = 0
	while get_distance() > (get_distance() + (get_distance()+new_dist)/2)/2:
		my_right(1)
		ang += 2
		my_fwd(1)
		new_dist = 30/math.cos(ang*180/math.pi)
	my_left(ang)
	a = raw_input()

def go_further(dist):
	print "going further"
	#go closer
	new_dist = dist
	ang = 0
	while get_distance() < (get_distance()+new_dist)/2:
		my_left(1)
		ang += 2
		my_fwd(1)
		new_dist = 30/math.cos(ang*180/math.pi)
	my_right(ang)
	a = raw_input()

def calcAngleFromDiff(diff):#sets the angle depending on the distance of the bot from the wall
	if diff < 2:
		return 7
	elif diff < 5:
		return 9
	elif diff < 10:
		return 11
	else: return 13

def calcFixAngle(diff3):#sets the angle to fix in case of curvy walls
	return diff3 * 2 + 2 #pattent design by george

print "Difference\tLeft Speed\tRight Speed"
print "---\t---\t---"
print "fuck this"

def timer(no_seconds):
	ot = time.time()
	while(time.time() - ot < no_seconds):    #running while loop for no_seconds seconds
		BrickPiUpdateValues()            # Ask BrickPi to update values for sensors/motors
		time.sleep(.1)                   # sleep for 100 ms

while True:
	
	diff = get_distance() - DESIRED_DISTANCE
	print diff

	if abs(diff) < 1:
		#Perfect
		#BrickPi.MotorSpeed[PORT_A] = BASE_SPEED_LEFT
		#BrickPi.MotorSpeed[PORT_B] = BASE_SPEED_RIGHT
		fwd(3)
	else: #bot needs to move
		if diff > 0: #go closer
			go_closer(get_distance())
		else: #go further
			go_further(get_distance())
