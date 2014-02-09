from BrickPi import *
import math
from self_adjusting_utilities import *

SONAR = PORT_1
DESIRED_DISTANCE = 30 #cm

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

while len (distance_measurements) < 9: #should be odd if integer results are desired
  result = BrickPiUpdateValues()
  if not result:
    distance_measurements.insert(0, BrickPi.Sensor[SONAR])

while True:
  result = BrickPiUpdateValues()
  if not result:
    #calculate median distance over last 10 results
    distance_measurements.pop()
    distance_measurements.insert(0, BrickPi.Sensor[SONAR])
    distance = median(distance_measurements)
    if distance > DESIRED_DISTANCE:
      print "too far away" #set 'proportional gain' speed
    elif distance < DESIRED_DISTANCE:
      print "too close" #set 'proportional gain speed backwards
    else:
      print "correct distance" #stop
