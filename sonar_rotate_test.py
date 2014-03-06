#!/usr/bin/python

from BrickPi import *
import sys, time

BrickPiSetup()  # setup the serial port for communication

motor = PORT_B

BrickPi.MotorEnable[motor] = 1 #Enable the Motor A

def getEncoderReading():
  return BrickPi.Encoder[motor]

def setMotorSpeed(amount):
  BrickPi.MotorSpeed[motor] = amount
  BrickPiUpdateValues()

def rotate():
  print "Encoder:", getEncoderReading()
  setMotorSpeed(30)
  time.sleep(0.8)
  setMotorSpeed(0)
  print "After:", getEncoderReading()

while(True):
  rotate()
  time.sleep(0.5)
