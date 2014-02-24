#!/usr/bin/python

# week 4, q2.2: Path Following !

import motion, math

TARGET_RADIUS = 5

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

waypoints2 = []
for (i, e) in enumerate(waypoints):
  waypoints2.append(e)
  if i != len(waypoints)-1:
    waypoints2.append( ((e[0]+waypoints[i+1][0]) / 2, (e[1]+waypoints[i+1][1]) / 2 ) )

for (x, y) in waypoints[1:]:
  (robotX, robotY, robotTheta) = motion.estimate_location()
  print "!!!!", x, y
  while (abs(robotX - x) > TARGET_RADIUS or abs(robotY - y) > TARGET_RADIUS):
    (robotX, robotY, robotTheta) = motion.estimate_location()
    motion.navigateToWaypoint(x, y)

