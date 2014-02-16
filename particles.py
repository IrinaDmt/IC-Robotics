import math
import random

NUMBER_OF_PARTICLES = 100
mu = 0
#below are standard deviations
sigma = 1 #straight line deviation 
# (average distance between how far our robot travelled and how far we wanted it to travel)
rotation_sigma = 1 #rotation deviation (in angles)
motor_sigma = 1 #angular deviation of our robot whilst driving in a straight line
#the above could be caused by one motor accidentally going slightly faster than another

particle_list = []

class Particle:
  def __init__(self, x, y, theta, weight):
    self.x = x
    self.y = y
    self.theta = theta
    self.weight = weight
    self.e = random.gauss(mu, sigma)
    self.f = random.gauss(mu, motor_sigma)
    self.g = random.gauss(mu, rotation_sigma)
  def update_forward(self, distance):
    theta_radians = (self.theta * 2 * math.pi) / 360
    self.x = self.x + (distance + self.e)*math.cos(theta_radians)
    self.y = self.y + (distance + self.e)*math.sin(theta_radians)
    self.theta = self.theta + self.f
  def update_rotation(self, angle):
    self.theta = self.theta + angle + self.g
  def state_tuple(self):
    return self.x, self.y, self.theta

#import these using "import particles",
# then call using namespace identifier, e.g. particles.initialise()
def initialise():
  for i in range(NUMBER_OF_PARTICLES):
    particle_list.append(Particle(0,0,0,0)) #change this if you want to change the origin
#e.g. change Particle(0,0,0,0) to Particle(100, 500, 0, 0) for origin at (100, 500)

def draw():
  particle_tuples = []
  for p in particle_list:
    particle_tuples.append( (p.x, p.y, p.theta) )
  print "drawParticles:" + str(particle_tuples)

def update_forward(distance):
  for p in particle_list:
    p.update_forward(distance)

def update_rotate(angle):
  for p in particle_list:
    p.update_rotation(angle)
