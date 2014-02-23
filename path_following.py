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
    print "Target Location: ", x, y

    (self.x, self.y, self.angle) = motion.estimate_location()

    print "Current Location: ", self.x, self.y

    dx = x - self.x
    dy = y - self.y
    distance = math.sqrt(dx**2 + dy**2)
    theta_portion = math.fabs(math.degrees(math.atan(dy / dx)))

    print "Current Angle: ", self.angle

    target_theta = 0
    if dx > 0 and dy > 0:
      target_theta = 360 - theta_portion
    elif dx > 0 and dy < 0:
      target_theta = theta_portion
    elif dx < 0 and dy > 0:
      target_theta = 180 + theta_portion
    elif dx < 0 and dy < 0:
      target_theta = 180 - theta_portion

    print "Target Angle:", target_theta
    
    rotation_theta = target_theta - self.angle
    if rotation_theta > 180:
      rotation_theta = rotation_theta - 360
    elif rotation_theta < -180:
      rotation_theta = rotation_theta + 360

    print "Rotation Angle:", rotation_theta

    print self.x, self.y, self.angle, rotation_theta, distance
    motion.rotate(rotation_theta)
    motion.fwd_amt(distance)
    motion.stop()

  def nnavigateToWaypoint(self, x, y):
    # given current X, Y, theta..
    (self.x, self.y, self.angle) = motion.estimate_location()
    print "Current position: (",self.x,",", self.y,",", self.angle,")"
    dx = x - self.x
    dy = y - self.y
    forward_distance = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
    absolute_angle = math.degrees(math.atan(dx / dy))
    print dx, dy, ">", forward_distance, absolute_angle
    diff_angle = absolute_angle - self.angle
    diff_angle = diff_angle % 360
    print "Rotating", diff_angle
    motion.rotate(diff_angle)
    motion.fwd_amt(forward_distance)
    motion.stop()

robby = PathFollower()
print "A:", motion.estimate_location()
robby.navigateToWaypoint(30, 30)
print "B:", motion.estimate_location()
robby.navigateToWaypoint(30, -20)
print "C:", motion.estimate_location()
robby.navigateToWaypoint(0, 0)
print "D:", motion.estimate_location()
