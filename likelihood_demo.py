import particles
import particles_addition
import random
import odometry

particlesList = []
#init 100 random particles 
for i in xrange(100):
  particlesList.append(particles.Particle(random.randint(0,3), random.randint(0,3), 90, 0.01))

for (i, p) in enumerate(particlesList):
	v = particles_addition.calculate_likelihood(p.x, p.y, p.theta, 168)
	print "coord: ", p.x, p.y, p.theta
	print "likelihood", v
 
