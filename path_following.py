#!/usr/bin/python

# week 4, q2.2: Path Following !

import motion, math

class PathFollower:
  
  def __init__(self, startX=0, startY=0, startAngle=0):
    # Constructor
    self.x = startX
    self.y = startY
    self.angle = startAngle

  def navigateToWaypoint(self, x, y):
    (self.x, self.y, self.angle) = motion.estimate_location()
    dx = x - self.x
    dy = y - self.y
    distance = math.sqrt(dx**2 + dy**2)
    theta_portion = abs(math.degrees(math.atan(dy / dx))) - self.angle
    
    print "Angle1:", theta_portion

    target_theta = 0
    if dx > 0 and dy > 0:
      target_theta = 360 - theta_portion
    elif dx > 0 and dy < 0:
      target_theta = theta_portion
    elif dx < 0 and dy > 0:
      target_theta = 180 + theta_portion
    elif dx < 0 and dy < 0:
      target_theta = 180 - theta_portion

    print "Angle2:", target_theta
    
    rotation_theta = 0
    if target_theta < self.angle:
      rotation_theta = (90 - self.angle) + target_theta
    elif target_theta > self.angle:
      rotation_theta = target_theta - self.angle

    print "Angle3:", rotation_theta
    
    rotation_theta = rotation_theta % 360

    print self.x, self.y, self.angle, rotation_theta, distance
    motion.rotate(rotation_theta)
    motion.fwd_amt(distance)

  def shittyNavigateToWaypoint(self, x, y):
    # given current X, Y, theta..
    (self.x, self.y, self.angle) = motion.estimate_location()
    print "Current position: (",self.x,",", self.y,",", self.angle,")"
    dx = x - self.x
    dy = y - self.y
    forward_distance = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
    absolute_angle = math.degrees(math.atan(dx / dy))
    print dx, dy, ">", forward_distance, absolute_angle
    absolute_angle = absolute_angle % 360
    diff_angle = self.angle - absolute_angle
    print "Rotating", diff_angle
    motion.rotate(diff_angle)
    motion.fwd_amt(forward_distance)


robby = PathFollower()
print "A:", motion.estimate_location()
robby.shittyNavigateToWaypoint(50, 50)
print "B:", motion.estimate_location()
robby.shittyNavigateToWaypoint(50, -20)
print "C:", motion.estimate_location()
robby.shittyNavigateToWaypoint(0, 0)
print "D:", motion.estimate_location()
