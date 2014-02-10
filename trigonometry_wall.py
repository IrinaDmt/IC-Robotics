#!/usr/bin/python
from BrickPi import *
import math
from self_adjusting_utilities import *
import sys

SONAR = PORT_1
DESIRED_DISTANCE = 30 #cm
INIT_SPEED = 100
SENSOR_SAMPLE_COUNT = 5
AXLE_DIAMETER = 15.6

motor1 = PORT_A
motor2 = PORT_B

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
	print "all ", distance_measurements
	return distance

#initialise to medium speeds at the beggining of the program
BrickPi.MotorSpeed[PORT_A] = INIT_SPEED
BrickPi.MotorSpeed[PORT_B] = INIT_SPEED + 2

sum = 200

BASE_SPEED_LEFT = 100
BASE_SPEED_RIGHT = 90
	

def turn90():
  angle = 90
  radius = get_distance() + AXLE_DIAMETER
  distance = angle * radius * math.pi / 180 #to radians
  BrickPiUpdateValues()
  dist_init = BrickPi.Encoder[motor1]
  no_rotations = distance / (2 * math.pi * WHEELRADIUS)
  degrees = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = BASE_SPEED_LEFT
  BrickPi.MotorSpeed[motor2] = BASE_SPEED_RIGHT
  print distance
  while BrickPi.Encoder[motor1] - dist_init < degrees:
    BrickPiUpdateValues()
    time.sleep(0.001)

def calcAngleFromDiff(diff):#sets the angle depending on the distance of the bot from the wall
	if diff < 2:
		return 3
	elif diff < 5:
		return 5
	elif diff < 10:
		return 8
	else: return 11 

def calcFixAngle(diff3):#sets the angle to fix in case of curvy walls
	return diff3 * 2 + 2 #pattent design by george

'''#Move Forward
 34 def fwd(distance):
 35   global WHEELRADIUS, speed_left, speed_right
 36   BrickPiUpdateValues()
 37   offset_1 = BrickPi.Encoder[motor1]
 38   offset_2 = BrickPi.Encoder[motor2]
 39   speed_left = 200
 40   speed_right = 204
 41   circumference = 2 * math.pi * WHEELRADIUS
 42   print "- Going forward ", distance, " cm"
 43   no_rotations = distance / circumference
 44   degrees  = no_rotations * 720
 45   BrickPi.MotorSpeed[motor1] = speed_left
 46   BrickPi.MotorSpeed[motor2] = speed_right
 47   print "deg", degrees, no_rotations
 48   while(BrickPi.Encoder[motor1] - offset_1 < degrees
 49     and BrickPi.Encoder[motor2] - offset_2 < degrees): # running while loop for no_seconds seconds
 50     BrickPiUpdateValues()               # Ask BrickPi to update values for sensors/motors
 51     adjustValues(degrees, offset_1, offset_2)
 52     time.sleep(.001)                    # sleep for 100 ms
 53     
 '''


print "Difference\tLeft Speed\tRight Speed"
print "---\t---\t---"

'''while True:
	
	diff = get_distance() - DESIRED_DISTANCE
	
	if abs(diff) < 3:
		#Perfect
		#BrickPi.MotorSpeed[PORT_A] = BASE_SPEED_LEFT
		#BrickPi.MotorSpeed[PORT_B] = BASE_SPEED_RIGHT
		fwd(3)
	else: #bot needs to move
		angle = calcAngleFromDiff(diff)
		if diff > 0: #go closer
			right(angle)
			fwd(math.sin(angle)*abs(diff))
			left(angle)
			idiff2 = get_distance() - DESIRED_DISTANCE
			if diff2 >= diff: #check curvy wall
				angle2 = calcFixAngle(diff2-diff)
				right(angle2)
		else: #go further
			left(angle)
			fwd(math.sin(angle)*abs(diff))
			right(angle)
			diff2 = get_distance() - DESIRED_DISTANCE
			if diff2 <= diff: #check curvy wall
				angle2 = calcFixAngle(diff2-diff)
				left(angle2)
	#time.sleep(0.3)



'''
turn90()





