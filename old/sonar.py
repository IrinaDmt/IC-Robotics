from BrickPi import *
import math
from self_adjusting_utilities import *

SONAR = PORT_1
DESIRED_DISTANCE = 30 #cm
INIT_SPEED = 200

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

def get_distance():
  global distance_measurements
  #calculate median distance over last 10 results
  distance_measurements.pop()
  distance_measurements.insert(0, BrickPi.Sensor[SONAR])
  distance = median(distance_measurements)
  print "Median ", distance
#  print "all ", distance_measurements
  return distance

#initialise to medium speeds at the beggining of the program
while True:
  while get_distance() > 60:
    BrickPi.MotorSpeed[PORT_A] = INIT_SPEED
    BrickPi.MotorSpeed[PORT_B] = INIT_SPEED + 2
    BrickPiUpdateValues()
  diff = get_distance() - DESIRED_DISTANCE
  if diff > 1 or diff < -1:
    const = abs(INIT_SPEED / diff)
  else:
    const = 0
  speed = (diff - 1) * const
  BrickPi.MotorSpeed[PORT_A] = speed
  BrickPi.MotorSpeed[PORT_B] = speed + 2
  while diff > 1 or diff < -1:
    print diff
    diff = get_distance() - DESIRED_DISTANCE
    if speed > 0:
      base_speed = 50
    else:
      base_speed = -50
    speed = ((diff - 1) * const) + base_speed
    if speed < 50 and diff > 0:
      speed = 50
    elif speed > -50 and diff < 0:
      speed = -50
    set_speeds(speed, speed+2)
    BrickPi.MotorSpeed[PORT_A] = speed
    BrickPi.MotorSpeed[PORT_B] = speed + 2

  stop() #If the difference is zero.
