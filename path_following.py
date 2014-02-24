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
    global negative_particles, positive_particles

    (self.x, self.y, self.angle) = motion.estimate_location()

    print "Navigating from (",self.x,", ",self.y,") -> (",x,", ",y,")"
    dx = x - self.x
    dy = y - self.y
    distance = math.sqrt(dx**2 + dy**2)
    theta_portion = math.fabs(math.degrees(math.atan(dy / dx)))

    print "Current Angle: ", self.angle

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
    
    rotation_theta = target_theta - self.angle
    if rotation_theta > 180:
      rotation_theta = rotation_theta - 360
    elif rotation_theta < -180:
      rotation_theta = rotation_theta + 360

    print "Rotation Angle:", rotation_theta

    motion.rotate(rotation_theta)
    motion.fwd_amt(distance)
    motion.stop()

gb = PathFollower()
waypoints = [
  (84, 30),
  (180, 30),
  (180, 54),
  (126, 54),
  (126, 168),
  (126, 126),
  (30, 54),
  (84, 54),
  (84, 30)
]

for (x, y) in waypoints[1:]:
  gb.navigateToWaypoint(x, y)
