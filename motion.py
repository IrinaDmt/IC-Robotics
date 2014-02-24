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
import math, sys, particles

WHEELRADIUS = 2.2
circumference = 2 * math.pi * WHEELRADIUS

BrickPiSetup()  # setup the serial port for communication

motor1 = PORT_A
motor2 = PORT_B
SONAR_PORT = PORT_1
speed_left = 0 
speed_right = 0
no_seconds_forward = 0.8775 # 30 cm
no_seconds_left = 1.03 # 90 deg
particle_counter = 0
turn_counter = 0

BrickPi.MotorEnable[motor1] = 1 #Enable the Motor A
BrickPi.MotorEnable[motor2] = 1 #Enable the Motor B

# Reset the motor sensor reading
BrickPi.Encoder[motor1] = 0
BrickPi.Encoder[motor2] = 0

BrickPi.SensorType[SONAR_PORT] = TYPE_SENSOR_ULTRASONIC_CONT

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi
particles.initialise()

def get_sonar_distance():
  return BrickPi.Sensor[SONAR_PORT]

def checkToDraw(offset):
  global particle_counter, circumference

  if particle_counter >= 250:
    distance = circumference * (BrickPi.Encoder[motor1] - offset) / 720
    particles.update_forward(distance)
    particles.update_probability(get_sonar_distance())
    particles.draw()
    particle_counter = 0

def fwd_amt(distance):
  global WHEELRADIUS, speed_left, speed_right, particle_counter, circumference
  BrickPiUpdateValues()
  offset_1 = BrickPi.Encoder[motor1]
  offset_2 = BrickPi.Encoder[motor2]
  speed_left = 200
  speed_right = 204
  print "- Going forward ", distance, " cm"
  no_rotations = distance / circumference
  degrees  = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right

  throttle_index = 0
  previous_offset = offset_1
  while(BrickPi.Encoder[motor1] - offset_1 < degrees
    and BrickPi.Encoder[motor2] - offset_2 < degrees): # running while loop for no_seconds seconds
    BrickPiUpdateValues()                # Ask BrickPi to update values for sensors/motors
    adjustValues(degrees, offset_1, offset_2)
    throttle_index += 1
    delta_distance = (circumference * (BrickPi.Encoder[motor1] - previous_offset) / 720)
    if delta_distance > 10:
      particles.update_forward(delta_distance)
      particles.update_probability(get_sonar_distance())
      #print "Moved", delta_distance, "cm - updating particle map"
      previous_offset = BrickPi.Encoder[motor1]
      particles.draw()
      throttle_index = 0
    
    time.sleep(.001)                       # sleep for 100 ms
  #needs to update last bit of movement, else particles will be off by up to 10 units
  BrickPiUpdateValues()
  delta_distance = (circumference * (BrickPi.Encoder[motor1] - previous_offset) / 720)
  particles.update_forward(delta_distance)
  particles.update_probability(get_sonar_distance())
  particles.draw()
 
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
  #print ">> L:", speed_left, "(",(rot1 / degrees * 100),"%) R:", speed_right, "(",(rot2 / degrees * 100),"%)"

def rotate(angle):
  if(angle >= 0):
    turn(angle, 'l')
  else:
    turn(-angle, 'r')

#Turn -- private function
def turn(deg, orientation):
  global WHEELRADIUS, speed_left, speed_right, turn_counter
  
  if deg < 1:
    # Angle is sufficiently small to just ignore. :)
    return

  turn_counter = 0
  #Adjust initial speeds
  if (orientation == "l"):
    speed_left = -100
    speed_right = 100 
  elif (orientation == "r"):
    speed_left = 100
    speed_right = -100
  else:
    raise Exception("undefined orientation")

  #Establish number of spins
  axle = 7.9
  distance = axle * 2 * math.pi * deg / 360 
  circumference = 2 * math.pi * WHEELRADIUS
  no_rotations = distance / circumference
  degrees  = no_rotations * 720 
  
  BrickPiUpdateValues()
  offset_1 = BrickPi.Encoder[motor1]
  offset_2 = BrickPi.Encoder[motor2]

  #Start turning 
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  #print "deg", degrees, no_rotations
  BrickPiUpdateValues()
  #time.sleep(.001)
  #turned = (BrickPi.Encoder[motor1] - offset_1) * WHEELRADIUS / (2 * axle)
  if orientation == 'l':
    particles.update_rotate(deg)
  else:
    particles.update_rotate(-deg)
  particles.update_probability(get_sonar_distance())
  particles.draw()
  while(abs(BrickPi.Encoder[motor1] - offset_1) < degrees
    and abs(BrickPi.Encoder[motor2] - offset_2) < degrees): 
    BrickPiUpdateValues()
    time.sleep(.001)
    #turnParticleDraw(turned)

def turnParticleDraw(turned):
  print turned
  global turn_counter
  turn_counter += 1
  if turn_counter >= 250:
    particles.update_rotate(turned)
    particles.update_probability(get_sonar_distance())
    particles.draw()
    turn_counter = 0


def estimate_location():
  return particles.estimate_location()

#Stop
def stop():
  print "- Stopping"
  BrickPi.MotorSpeed[motor1] = 0
  BrickPi.MotorSpeed[motor2] = 0
  BrickPiUpdateValues()
  timer(1)

#Timer
def timer(no_seconds):
  ot = time.time()
  while(time.time() - ot < no_seconds): # running while loop for no_seconds seconds
    BrickPiUpdateValues()                # Ask BrickPi to update values for sensors/motors
    time.sleep(.01)                       # sleep for 100 ms
'''
for i in range(1):
  input = raw_input(">")
  if input == "s": 
    back(2)
    stop()
  if input == "w":
    fwd_amt(30)
    stop()'''
