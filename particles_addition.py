import odometry
import random
import math, sys

robustness_constant = 0.05 #(5% chance of random sonar values)
sonar_sigma = 1

# --- per particle ---

def calculate_likelihood(x, y, theta, z):
  #decide wall & distance
  lowestDistance = sys.maxsize
  closestWall = odometry.walls[0]
  erer = '?'

  for (i, wall) in enumerate(odometry.walls):
        
    #print "curr wall", wall.x1, wall.y1, wall.x2, wall.y2, "wall number", i
    if wall.validIntersectionExistsFrom(x, y, theta) and wall.distanceFrom(x, y, theta) < lowestDistance:
      closestWall = wall
      lowestDistance = wall.distanceFrom(x, y, theta)
      erer = chr(ord('a') + i)
  
  #print "Facing wall", erer

  # Actual likelihood calculation
  m = closestWall.distanceFrom(x, y, theta)
  return math.exp((-(z - m)**2) / (2 * sonar_sigma**2)) + robustness_constant


# --- for all particles ---

