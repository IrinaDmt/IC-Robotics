#!/usr/bin/python

# 2.3: Sonar Investigation
#      - Continuously print values from sonar sensor

from __future__ import print_function
from BrickPi import *
import sys, time

READING_INTERVAL = 0.5
SONAR_PORT = PORT_1

BrickPiSetup()
BrickPi.SensorType[SONAR_PORT] = TYPE_SENSOR_ULTRASONIC_CONT
BrickPiSetupSensors()

def getSonarReading():
  return BrickPi.Sensor[SONAR_PORT]

sys.stdout.write("Reading sonar...\n")

i = 0
while(True):
  BrickPiUpdateValues()
  time.sleep(READING_INTERVAL)
  i += 1
  print("Sonar reading %i: %i" % (i, getSonarReading()), end='\r')
  sys.stdout.flush()
