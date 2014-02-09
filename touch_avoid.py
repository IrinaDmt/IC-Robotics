from BrickPi import *
import math
from self_adjusting_utilities import *

ROBOT_LENGTH = 30
AXLE_DIAMETER = 15

LEFT_BUMPER = PORT_2
RIGHT_BUMPER = PORT_1


BrickPiSetup()

BrickPi.SensorType[LEFT_BUMPER] = TYPE_SENSOR_TOUCH
BrickPi.SensorType[RIGHT_BUMPER] = TYPE_SENSOR_TOUCH

BrickPiSetupSensors()



while True:
  result = BrickPiUpdateValues()
  if not result:
    if BrickPi.Sensor[LEFT_BUMPER] and BrickPi.Sensor[RIGHT_BUMPER]:
      print "Front Collision"
      back(ROBOT_LENGTH) #back ROBOT_LENGTH cm

      #randomly choose left or right (try to avoid infinite loops)
     # if random.random() < 0.5:
     #   choice = "left"
     # else:
      choice = "right"

      if choice is "left":
        left(90)
        #fwd(AXLE_DIAMETER)
        #right(90)
      elif choice is "right":
        right(90)
        #fwd(AXLE_DIAMETER)
        #left(90)
      fwd(1) #continue going forward (return to loop)
    elif BrickPi.Sensor[RIGHT_BUMPER]:
      print "Right Collision"
      back(ROBOT_LENGTH) #back ROBOT_LENGTH cm
      left(90) #turn left 90 degrees
      #fwd(AXLE_DIAMETER) #forward AXLE_DIAMETER cm
      #right(90) #turn right 90 degrees
      #fwd(1) #return to loop
    elif BrickPi.Sensor[LEFT_BUMPER]:
      print "Left Collision"
      back(ROBOT_LENGTH) #back ROBOT_LENGTH cm
      right(90) #turn right 90 degrees
      #fwd(AXLE_DIAMETER) #forward AXLE_DIAMETER cm
      #left(90) #turn left 90 degrees
      #fwd(1) #return to loop
    else:
      fwd(1) #continue
