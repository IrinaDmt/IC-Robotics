#!/usr/bin/python

import motion, time

print "Running sonar_spin()"
readings, degrees = motion.sonar_spin()
time.sleep(2)
#motion.sonar_spin_back()
print len(readings)
print readings
print degrees
