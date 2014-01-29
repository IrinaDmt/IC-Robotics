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

BrickPiSetup()  # setup the serial port for communication

motor1 = PORT_A
motor2 = PORT_B
speed = 50

BrickPi.MotorEnable[motor1] = 1 #Enable the Motor A
BrickPi.MotorEnable[motor2] = 1 #Enable the Motor B

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

#Move Forward
def fwd(no_seconds):
  print "Going Forward"
  BrickPi.MotorSpeed[motor1] = -speed
  BrickPi.MotorSpeed[motor2] = -speed
  timer(no_seconds)

#Move Left
def left(no_seconds):
  print "- Going left"
  BrickPi.MotorSpeed[motor1] = -speed/2
  BrickPi.MotorSpeed[motor2] = speed/2
  timer(no_seconds)
  
#Move backward
def back(no_seconds):
  print "- Reversing"
  BrickPi.MotorSpeed[motor1] = speed
  BrickPi.MotorSpeed[motor2] = speed
  timer(no_seconds)
  
#Stop
def stop():
  print "- Stopping"
  BrickPi.MotorSpeed[motor1] = 0
  BrickPi.MotorSpeed[motor2] = 0

#Timer
def timer(no_seconds):
  ot = time.time()
  while(time.time() - ot < no_seconds):    #running while loop for no_seconds seconds
    BrickPiUpdateValues()            # Ask BrickPi to update values for sensors/motors
    time.sleep(.1)                   # sleep for 100 ms

while (raw_input("Enter 1 for a square or 0 to stop:") == 1):
  for i in range(4):
    fwd(3)
    left(2)
