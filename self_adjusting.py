#!/usr/bin/python
# Jaikrishna
# Initial Date: June 24, 2013
# Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor

from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import math, sys

WHEELRADIUS = 2.2

BrickPiSetup()  # setup the serial port for communication

motor1 = PORT_A
motor2 = PORT_B
speed_left = 0 
speed_right = 0
no_seconds_forward = 0.8775 # 30 cm
no_seconds_left = 1.03 # 90 deg

BrickPi.MotorEnable[motor1] = 1 #Enable the Motor A
BrickPi.MotorEnable[motor2] = 1 #Enable the Motor B

# Reset the motor sensor reading
BrickPi.Encoder[motor1] = 0
BrickPi.Encoder[motor2] = 0

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

#Move Forward
def fwd(no_seconds):
  global speed_left, speed_right
  print "- Going Forward"
  speed_right = 210
  speed_left = 200
  BrickPi.MotorSpeed[motor1] = speed_right
  BrickPi.MotorSpeed[motor2] = speed_left
  timer(no_seconds)

def fwd_amt(distance):
  global WHEELRADIUS, speed_left, speed_right
  BrickPiUpdateValues()
  # BrickPi.EncoderOffset[motor1] = BrickPi.Encoder[motor1]
  # BrickPi.EncoderOffset[motor2] = BrickPi.Encoder[motor2]
  offset_1 = BrickPi.Encoder[motor1]
  offset_2 = BrickPi.Encoder[motor2]
  speed_left = 200
  speed_right = 204
  circumference = 2 * math.pi * WHEELRADIUS
  print "- Going forward ", distance, " cm"
  no_rotations = distance / circumference
  degrees  = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right

  print "deg", degrees, no_rotations

  while(BrickPi.Encoder[motor1] - offset_1 < degrees
    and BrickPi.Encoder[motor2] - offset_2 < degrees): # running while loop for no_seconds seconds
    BrickPiUpdateValues()            	# Ask BrickPi to update values for sensors/motors
    adjustValues(degrees, offset_1, offset_2)
    time.sleep(.001)                   	# sleep for 100 ms
    
def adjustValues(degrees, offset_1, offset_2):
  global speed_left, speed_right
  rot1 = BrickPi.Encoder[motor1] - offset_1
  rot2 = BrickPi.Encoder[motor2] - offset_2
  target_speed = 202
  k = 1 # coefficient
  if rot1 < rot2:
    diff = rot2 - rot1
    speed_left = target_speed + diff * k
    speed_right = target_speed - diff * k
  elif rot1 > rot2: 
    diff = rot1 - rot2
    speed_left = target_speed - diff * k
    speed_right = target_speed + diff * k
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  print ">> L:", speed_left, "(",(rot1 / degrees * 100),"%) R:", speed_right, "(",(rot2 / degrees * 100),"%)"

#Move Left
def left(no_seconds):
  print "- Going left"
  global speed_left, speed_right
  speed_left = 80
  speed_right = -78
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  timer(no_seconds)
  
#Move backward
def back(no_seconds):
  global speed_left, speed_right
  print "- Reversing"
  speed_left = -200 
  speed_right = -200
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  timer(no_seconds)
  
#Stop
def stop():
  print "- Stopping"
  BrickPi.MotorSpeed[motor1] = 0
  BrickPi.MotorSpeed[motor2] = 0
  BrickPiUpdateValues()

#Turn 90 degrees left
def left90deg():
  global WHEELRADIUS, speed_left, speed_right
  axle = 6
  distance = axle * math.pi / 2 # distance for 90 degrees when the radius is axle
  BrickPiUpdateValues()
  offset_1 = BrickPi.Encoder[motor1]
  offset_2 = BrickPi.Encoder[motor2]
  speed_left = -200
  speed_right = 204
  circumference = 2 * math.pi * WHEELRADIUS
  print "- Going forward ", distance, " cm"
  no_rotations = distance / circumference
  degrees  = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right

  print "deg", degrees, no_rotations

  while(BrickPi.Encoder[motor1] - offset_1 < degrees
    and BrickPi.Encoder[motor2] - offset_2 < degrees): # running while loop for no_seconds seconds
    BrickPiUpdateValues()            	# Ask BrickPi to update values for sensors/motors
    adjustValuesLeft(degrees, offset_1, offset_2)
    time.sleep(.001)                   	# sleep for 100 ms
    
def adjustValuesLeft(degrees, offset_1, offset_2):
  global speed_left, speed_right
  rot1 = BrickPi.Encoder[motor1] - offset_1
  rot2 = BrickPi.Encoder[motor2] - offset_2
  target_speed = 202
  k = 1 # coefficient
  if rot1 < rot2:
    diff = rot2 - rot1
    speed_left = (-1) * (target_speed + diff * k)
    speed_right = target_speed - diff * k
  elif rot1 > rot2: 
    diff = rot1 - rot2
    speed_left = (-1) * (target_speed - diff * k)
    speed_right = target_speed + diff * k
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  print ">> L:", speed_left, "(",(rot1 / degrees * 100),"%) R:", speed_right, "(",(rot2 / degrees * 100),"%)"


#Timer
def timer(no_seconds):
  ot = time.time()
  while(time.time() - ot < no_seconds): # running while loop for no_seconds seconds
    BrickPiUpdateValues()            	# Ask BrickPi to update values for sensors/motors
    time.sleep(.01)                   	# sleep for 100 ms



for i in range(1):
  input = raw_input(">")
  if input == "s": 
    back(2)
    stop()
  if input == "w":
    fwd_amt(30)
    stop()
