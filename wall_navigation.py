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

while True:
  diff = get_distance() - DESIRED_DISTANCE

  sys.stdout.write("%i, " % diff)  

  if diff == 0:
    # Perfect
    BrickPi.MotorSpeed[PORT_A] = BASE_SPEED_LEFT
    BrickPi.MotorSpeed[PORT_B] = BASE_SPEED_RIGHT
  else:
    # Needs tweaking
    if abs(diff) > 5:
      amt = diff/2
    else:
      amt = diff
    BrickPi.MotorSpeed[PORT_A] = BASE_SPEED_LEFT + amt
    BrickPi.MotorSpeed[PORT_B] = BASE_SPEED_RIGHT - amt
    BrickPiUpdateValues()
    time.sleep(0.5)
    fwd(1)
  BrickPiUpdateValues()
