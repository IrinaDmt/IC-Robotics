import math, sys

class Wall:
  def __init__(self, x1, y1, x2, y2):
    self.x1 = x1
    self.x2 = x2
    self.y1 = y1
    self.y2 = y2

    if x1 > x2:
      self.maxX = x1
      self.minX = x2
    else:
      self.maxX = x2
      self.minX = x1

    if y1 > y2:
      self.maxY = y1
      self.minY = y2
    else:
      self.maxY = y2
      self.minY = y1

    self.Ydiff = y2 - y1
    self.Xdiff = x2 - x1

  def distanceFrom(self, x, y, theta):
    numerator   = self.Ydiff * (self.x1 - x) - self.Xdiff * (self.y1 - y)
    denominator = self.Ydiff * math.cos(math.radians(theta)) - self.Xdiff * math.sin(math.radians(theta))
    
    if denominator == 0:
      # Robot's direction vector and the wall do not intersect
      return sys.maxsize
    
    return numerator / denominator

  def validIntersectionExistsFrom(self, x, y, theta):
    m = self.distanceFrom(x, y, theta)
    
    if m == sys.maxsize or m <= 0:
      # If no intersection exists (infinte distance, lines are perpendicular)
      # or if the intersection is behind the robot
      return False
    
    intersectX = x + m * math.cos(math.radians(theta))
    intersectY = y + m * math.sin(math.radians(theta))
    return intersectX >= self.minX and intersectX <= self.maxX and intersectY >= self.minY and intersectY <= self.maxY 

  def incidenceAngleFrom(self, x, y, theta):
    inverseYdiff = self.y1 - self.y2
    numerator   = math.cos(math.radians(theta)) * inverseYdiff + math.sin(math.radians(theta)) * Xdiff
    denominator = math.sqrt(inverseYdiff**2 + Xdiff**2)
    return math.degrees(math.acos(numerator/denominator))
    

walls = [Wall(0,0,0,168), #a
  Wall(0,168,84,168), #b
  Wall(84,126,84,210), #c 
  Wall(84,210,168,210),#d
  Wall(168,210,168,84),#e
  Wall(168,84,210,84),#f
  Wall(210,84,210,0),#g
  Wall(210,0,0,0) ]#h
