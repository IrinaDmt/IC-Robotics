import odometry
import random, sys, math

NUMBER_OF_PARTICLES = 100
mu = 0
#below are standard deviations
sigma = 0.2 #straight line deviation 
# (average distance between how far our robot travelled and how far we wanted it to travel)
rotation_sigma = 0 #rotation deviation (in angles)
motor_sigma = 0.4 #angular deviation of our robot whilst driving in a straight line
#the above could be caused by one motor accidentally going slightly faster than another

robustness_constant = 0.05 #(5% chance of random sonar values)
sonar_sigma = 1 # 

particle_list = []

# A Canvas class for drawing a map and particles:
#     - it takes care of a proper scaling and coordinate transformation between
#      the map frame of reference (in cm) and the display (in pixels)
class Canvas:
  def __init__(self,map_size=210):
    self.map_size    = map_size;    # in cm;
    self.canvas_size = 768;         # in pixels;
    self.margin      = 0.05*map_size;
    self.scale       = self.canvas_size/(map_size+2*self.margin);

  def drawLine(self,line):
    x1 = self.__screenX(line[0]);
    y1 = self.__screenY(line[1]);
    x2 = self.__screenX(line[2]);
    y2 = self.__screenY(line[3]);
    print "drawLine:" + str((x1,y1,x2,y2))

  def drawParticles(self,data=None):
    if data is None:
      data = particle_list

    particle_tuples = []
    for p in data:
      particle_tuples.append( (self.__screenX(p.x), self.__screenY(p.y), p.theta) )
    print "drawParticles:" + str(particle_tuples)

  def __screenX(self,x):
    return (x + self.margin)*self.scale

  def __screenY(self,y):
    return (self.map_size + self.margin - y)*self.scale

# A Map class containing walls
class Map:
  def __init__(self):
    self.walls = [];

  def add_wall(self,wall):
    self.walls.append(wall);

  def clear(self):
    self.walls = [];

  def draw(self):
    for wall in self.walls:
      canvas.drawLine(wall);

canvas = Canvas();    # global canvas we are going to draw on

mymap = Map();
# Definitions of walls
# a: O to A
# b: A to B
# c: C to D
# d: D to E
# e: E to F
# f: F to G
# g: G to H
# h: H to O
mymap.add_wall((0,0,0,168))        # a
mymap.add_wall((0,168,84,168))     # b
mymap.add_wall((84,126,84,210))    # c
mymap.add_wall((84,210,168,210))   # d
mymap.add_wall((168,210,168,84))   # e
mymap.add_wall((168,84,210,84))    # f
mymap.add_wall((210,84,210,0))     # g
mymap.add_wall((210,0,0,0))        # h
mymap.draw()

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
    theta_radians = math.radians(self.theta)
    self.x += (distance + self.e)*math.cos(theta_radians)
    self.y += (distance + self.e)*(-math.sin(theta_radians)) #due to clockwise degrees
    self.theta = self.theta + self.f
  def update_rotation(self, angle):
    temp_theta = self.theta + angle + self.g
    if temp_theta < 0:
      self.theta = temp_theta + 360
    elif temp_theta > 360:
      self.theta = temp_theta - 360
  def state_tuple(self):
    return self.x, self.y, self.theta
  def calculate_likelihood(self, z):
    x = self.x
    y = self.y
    theta = self.theta

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

  def update_weight(self, z):
    self.weight *= self.calculate_likelihood(z)

#import these using "import particles",
# then call using namespace identifier, e.g. particles.initialise()
def initialise():
  for i in range(NUMBER_OF_PARTICLES):
    particle_list.append(Particle(0, 0, 0, 1.0 / NUMBER_OF_PARTICLES)) #change this if you want to change the origin
#e.g. change Particle(0,0,0,0) to Particle(100, 500, 0, 0) for origin at (100, 500)

def draw():
  canvas.drawParticles(particle_list)

def update_forward(distance):
  print "Updating forward ", distance
  for p in particle_list:
    p.update_forward(distance)

  # read from the sonar and update the particles' weights
  # update_probability(sonar_reading)

def update_rotate(angle):
  for p in particle_list:
    p.update_rotation(angle)
  # read from the sonar and update the particles' weights
  # update_probability(sonar_reading)

def estimate_location():
  x = 0
  y = 0
  theta = 0
  for p in particle_list:
    x     += p.x * p.weight
    y     += p.y * p.weight
    theta += p.theta * p.weight
  return x, y, theta

def normalise():
  global particle_list

  probability_sum = 0
  for p in particle_list:
    probability_sum += p.weight

  for p in particle_list:
    p.weight /= probability_sum
    
def resample():
  global particle_list, NUMBER_OF_PARTICLES

  normalise()

  # generate cumulative probability list
  cumul_prob_list = []
  cumul_prob = 0
  prev_prob = 0
  for p in particle_list:
    prev_prob = cumul_prob
    cumul_prob += p.weight
    cumul_prob_list.append((prev_prob, cumul_prob, p)) #triple

  # randomly choose new copied particle
  new_particles = []
  r = 0 # random number
  for i in range(len(particle_list)):
    r = random.random() #0.0-1.0
    for c in cumul_prob_list:
      if r < c[1] and r >= c[0]: #c[0] = lower bound for this particle, c[1] = upper bound
        new_particles.append(
          Particle(c[2].x, c[2].y, c[2].theta, 1.0/NUMBER_OF_PARTICLES)
        ) # c[2] = old particle
        break
    else: # else belonging to for loop - check python documentation if confused
      # if no particle found in cpl, throw error
      print "Error: no particle found for probability ", r

  #overwrite list
  particle_list = new_particles


def update_probability(sonar_distance):
  for p in particle_list:
    p.calculate_likelihood(sonar_distance)
  resample()
  
def demo_resampling_and_normalising():
  global particle_list
  sample_size = NUMBER_OF_PARTICLES
  sonar = 168
  particle_list = []
  for i in xrange(sample_size):
    particle_list.append(Particle(random.randint(0,3), random.randint(0,3), 90, 0.01))
    particle_list[i].update_weight(sonar)
    print "Particle coordinates are :", particle_list[i].x, particle_list[i].y
    print "New weight is", particle_list[i].weight

  print
  print "##### normalising"
  print 

  normalise()
  for i in xrange(sample_size):
    print "Particle coordinates are :", particle_list[i].x, particle_list[i].y
    print "New weight is", particle_list[i].weight

  print
  print "##### resampling"
  print

  resample()
  for i in xrange(sample_size):
    print "Particle coordinates are :", particle_list[i].x, particle_list[i].y
    print "New weight is", particle_list[i].weight
  particle_list = []
    
