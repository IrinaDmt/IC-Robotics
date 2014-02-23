import particles
import particles_addition
import random
import odometry

particlesList = []
#init 100 random particles 
for i in xrange(1):
  particlesList.append(particles.Particle(0, 0, 0, 1))
    
#sample sonar reading
sonar = 200

for (i, p) in enumerate(particlesList):
    print "Particle", i, ":"
    print particles_addition.calculate_likelihood(p.x, p.y, p.theta, sonar)
    #print "x:", p.x, "y:", p.y
    #print
