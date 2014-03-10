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
SONAR_PORT = PORT_4
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

class Motor:
  def __init__(self, port):
    self.port = port
    self.offset = 0
    
    self.enableMotor()
    self.resetOffset()

  def enableMotor(self):
    BrickPi.MotorEnable[self.port] = 1
    BrickPiUpdateValues()
  
  def resetOffset(self):
    BrickPiUpdateValues()
    offset = self.offset = BrickPi.Encoder[self.port]

  def getOffset(self):
    BrickPiUpdateValues()
    return BrickPi.Encoder[self.port] - self.offset

  def getOffsetDegrees(self):
    return self.getOffset() / 2

  def setSpeed(self, speed):
    BrickPi.MotorSpeed[self.port] = speed
    BrickPiUpdateValues()

  def stop(self):
    self.setSpeed(0)

class SonarMotor:
  def __init__(self, port, cog_ratio=(7.0/34.5)): # 7 / 40 is the actual ratio, but we tweak values!
    self.motor = Motor(port)

    # Number of notches on motor cog / Number of notches on sonar cog
    print "Ratio =", cog_ratio
    self.ratio = cog_ratio

    self.spin_speed = 50
    self.min_callback_angle = 3

  def setSpinSpeed(self, spin_speed):
    self.spin_speed = spin_speed

  def setMinCallbackAngle(self, angle):
    self.min_callback_angle = angle
  
  def angleMotorToSensor(self, motor_degrees):
    return motor_degrees * self.ratio

  def angleSensorToMotor(self, sensor_degrees):
    return sensor_degrees / self.ratio

  def getSonarOffsetDegrees(self):
    return self.angleMotorToSensor(self.motor.getOffsetDegrees())

  def rotateClockwise(self, angle, callback=None):
    # Reset the motor's current offset to 0
    self.motor.resetOffset()

    # Remember the starting offset (should be 0!)
    offset = previous_offset = self.getSonarOffsetDegrees()

    # Spin up the motor
    self.motor.setSpeed(self.spin_speed)

    while(offset <= angle):
      offset = self.getSonarOffsetDegrees()
      diff = offset - previous_offset
      
      if diff >= self.min_callback_angle:
        # Callback!
	if callback:
	  callback(diff)
	previous_offset = offset
      time.sleep(0.01)
    self.motor.stop()


  def rotateAnticlockwise(self, angle, callback=None):
    self.motor.resetOffset()

    offset = previous_offset = self.getSonarOffsetDegrees()
    self.motor.setSpeed(-self.spin_speed)

    while(offset > -angle):
      offset = self.getSonarOffsetDegrees()
      diff = abs(offset - previous_offset)
      
      if diff >= self.min_callback_angle:
        if callback:
          callback(diff)
	previous_offset = offset
      time.sleep(0.01)
    self.motor.stop()
    

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
      #particles.update_forward(delta_distance)
      #particles.update_probability(get_sonar_distance())
      #print "Moved", delta_distance, "cm - updating particle map"
      previous_offset = BrickPi.Encoder[motor1]
      #particles.draw()
      throttle_index = 0

      # HACK!!! we are going to repeatedly call navigateToWaypoint() in path_following,py
      #return
    
    time.sleep(.001)                       # sleep for 100 ms
  #needs to update last bit of movement, else particles will be off by up to 10 units
  BrickPiUpdateValues()
  delta_distance = (circumference * (BrickPi.Encoder[motor1] - previous_offset) / 720)
  #particles.update_forward(delta_distance)
  #particles.update_probability(get_sonar_distance())
  #particles.draw()
 
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
  axle = 7
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
  while(abs(BrickPi.Encoder[motor1] - offset_1) < degrees
    and abs(BrickPi.Encoder[motor2] - offset_2) < degrees): 
    BrickPiUpdateValues()
    time.sleep(.0001)
  stop()

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

def set_location(x, y, angle):
  particles.initialise(x, y, angle)

def navigateToWaypoint(x, y):
  (currentX, currentY, currentAngle) = particles.estimate_location()

  print "Navigating from (",currentX,", ",currentY,") -> (",x,", ",y,")"
  dx = x - currentX
  dy = y - currentY
  distance = math.sqrt(dx**2 + dy**2)
  theta_portion = math.fabs(math.degrees(math.atan(dy / dx)))

  print "Current Angle: ", currentAngle

  target_theta = 0
  if dx > 0 and dy > 0:
    #target_theta = 360 - theta_portion
    target_theta = theta_portion
  elif dx > 0 and dy < 0:
    #target_theta = theta_portion
    target_theta = 360 - theta_portion
  elif dx < 0 and dy > 0:
    #target_theta = 180 + theta_portion
    target_theta = 180 - theta_portion
  elif dx < 0 and dy < 0:
    #target_theta = 180 - theta_portion
    target_theta = 180 + theta_portion

  print "Target Angle:", target_theta
    
  rotation_theta = target_theta - currentAngle
  if rotation_theta > 180:
    rotation_theta = rotation_theta - 360
  elif rotation_theta < -180:
    rotation_theta = rotation_theta + 360
  
  print "Rotation Angle:", rotation_theta

  rotate(rotation_theta)
  forward_amount = min(distance, 20)
  fwd_amt(forward_amount)
  stop()
  time.sleep(0.05)
  particles.update_forward(forward_amount)
  for i in range(0,9):
    sonar_reading = get_sonar_distance()
    if sonar_reading < 255:
      particles.update_probability(sonar_reading)
      break
    else:
      time.sleep(0.1)
  else:
    particles.update_probability(get_sonar_distance())

  particles.draw()

#Stop
def stop():
  print "- Stopping"
  BrickPi.MotorSpeed[motor1] = 0
  BrickPi.MotorSpeed[motor2] = 0
  BrickPiUpdateValues()
  timer(1)


# Create a new motor for our sonar motor
sonar_motor = Motor(PORT_C)

def sonar_spin_back():
  # C0nfig params
  SPIN_SPEED    = 40 

  # Get start orientation
  sonar_motor.resetOffset() 

  # Remember the starting offset
  offset = previous_offset = sonar_motor.getOffsetDegrees()
  
  time.sleep(1)
  sonar_motor.resetOffset()

  # Start spinning
  sonar_motor.setSpeed(SPIN_SPEED)

  # When we've span X degrees, take another reading
  while(offset < 360):
    offset = sonar_motor.getOffsetDegrees()
    diff = abs(offset - previous_offset)
    if False and diff > 310 and diff < 330:
      sonar_motor.stop()
      time.sleep(0.3)
      sonar_motor.setSpeed(int(SPIN_SPEED*0.8))
      previous_offset = offset
    BrickPiUpdateValues()
    
  sonar_motor.stop()

##############

somo = SonarMotor(PORT_C)

def sonar_spin():
  readings = []
  intervals = []

  def sonar_spin_callback(diff):
    readings.append(get_sonar_distance())
    intervals.append(diff)

  somo.rotateAnticlockwise(360, sonar_spin_callback)
  
  return readings, intervals


##############

def sonar_spin_old():
  # Configuration parameters for sonar_spin()
  SPIN_SPEED    = -100
  READ_INTERVAL = 6  # degrees

  # Get start orientation
  sonar_motor.resetOffset() 

  # Get a reading
  start_reading = get_sonar_distance()
  
  # Initialise list to store readings in
  readings = []
  degrees = []

  # Remember the starting offset
  offset = previous_offset = sonar_motor.getOffsetDegrees()
  
  if offset != 0:
    time.sleep(1)
    sonar_motor.resetOffset()

  # Start spinning
  print "Spinning forward from offset", offset
  sonar_motor.setSpeed(SPIN_SPEED)
  init_offset = offset

  counter = 0 # every 10 sonar intervals, stop and wait
  # When we've span X degrees, take another reading
  while(offset >= -360):
    offset = sonar_motor.getOffsetDegrees()
    diff = abs(offset - previous_offset)
    if diff >= READ_INTERVAL:
      readings.append(get_sonar_distance())
      degrees.append(previous_offset - offset)
      previous_offset = offset
      counter += 1
      #if counter % 10 == 0:
      #  sonar_motor.stop()
      #  time.sleep(0.4)
      #  sonar_motor.setSpeed(SPIN_SPEED)
    if diff <= 0:
      print "jammed"
    BrickPiUpdateValues()
  
  print "......."

  sonar_motor.stop()

  # Return the list of all the values.
  return readings, degrees

#Timer
def timer(no_seconds):
  ot = time.time()
  while(time.time() - ot < no_seconds): # running while loop for no_seconds seconds
    BrickPiUpdateValues()                # Ask BrickPi to update values for sensors/motors
    time.sleep(.01)                       # sleep for 100 ms

