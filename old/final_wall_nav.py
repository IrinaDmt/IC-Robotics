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

BASE_SPEED_LEFT = 70
BASE_SPEED_RIGHT = 71

# Delay next action until this time
delay_reading = 0
delay_callback = None

def wait(seconds, callback = None):
  global delay_reading
  delay_reading = time.time() + seconds
  delay_callback = callback

BASE_AMT = 3
const = 2
motorLeft = PORT_A
motorRight = PORT_B

#Timer 
def timer(no_seconds): 
  ot = time.time() 
  while(time.time() - ot < no_seconds):    #running while loop for no_seconds seconds 
    BrickPiUpdateValues()            # Ask BrickPi to update values for sensors/motors 
    time.sleep(.1)                   # sleep for 100 ms 

def bound(amt):
  if amt < BASE_AMT:
    return BASE_AMT
  elif amt > 7:
    return 7
  return amt

#Tweakin
direction = 0 

while True:
  BrickPiUpdateValues()
  
  diff = get_distance() - DESIRED_DISTANCE

  print diff

  if abs(diff) <= 1:
    # Perfect
    BrickPi.MotorSpeed[motorLeft] = BASE_SPEED_LEFT
    BrickPi.MotorSpeed[motorRight] = BASE_SPEED_RIGHT

  elif diff > 1:
    # Needs tweaking
    diff = get_distance() - DESIRED_DISTANCE
    amt = int(BASE_AMT + diff * const) 
    amt = bound(amt)
    l_amt = 0
    if direction == -1:
      l_amt = amt/2
    print "amt ", amt
    BrickPi.MotorSpeed[motorLeft] = BASE_SPEED_LEFT + amt + l_amt
    BrickPi.MotorSpeed[motorRight] = BASE_SPEED_RIGHT - amt
    timer(0.2) 
    
    # After turning go forward more than the amount of turn
    BrickPi.MotorSpeed[motorLeft] = BASE_SPEED_LEFT
    BrickPi.MotorSpeed[motorRight] = BASE_SPEED_RIGHT
    timer(0.4)
 #   direction = 1

  elif diff < -1:
    diff = get_distance() - DESIRED_DISTANCE
    amt = int(BASE_AMT + (-1) * diff * const) 
    amt = bound(amt)
    r_amt = 0
    if direction == 1:
      r_amt = amt/2
    print "amt ", amt
    BrickPi.MotorSpeed[motorLeft] = BASE_SPEED_LEFT - amt
    BrickPi.MotorSpeed[motorRight] = BASE_SPEED_RIGHT + amt + r_amt
    timer(0.2) 
    
    # After turning go forward more than the amount of turn
    BrickPi.MotorSpeed[motorLeft] = BASE_SPEED_LEFT
    BrickPi.MotorSpeed[motorRight] = BASE_SPEED_RIGHT
    timer(0.3)

##    direction = -1
    # After turning, we want to turn it back..
    '''BrickPi.MotorSpeed[PORT_A] = BASE_SPEED_LEFT + amt
    BrickPi.MotorSpeed[PORT_B] = BASE_SPEED_RIGHT - amt
    print "turning back"
    wait(0.1)'''
  BrickPiUpdateValues()
