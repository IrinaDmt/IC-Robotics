#!/usr/bin/python

from motion import *
from fractions import gcd
from math import *
robo_name = '''

 _______               __                      __    
|     __|.--.--.--.--.|  |--.----.--.--.-----.|  |--.
|    |  ||  |  |  |  ||  _  |   _|  |  |__ --||     |
|_______||_____|___  ||_____|__| |_____|_____||__|__|
               |_____|'''

locations = [1, 2, 4, 5, 7]
loc_sigs = {1:None, 2:None, 4:None, 5:None, 7:None}
dep_hists = {1:None, 2:None, 4:None, 5:None, 7:None}
SONAR_STEP = 6

class DepthHistogram(object):
    
    def __init__(self):
        self.frequencies = {}
        for i in xrange(256):
            self.frequencies[i] = 0
    
    def updateFreq(self, depth):
        self.frequencies[depth] += 1

    def setFrequenciesFromDict(self, dict):
        for k, v in dict.iteritems():
	  self.frequencies[k] = v

    def getFrequencies(self):
        return self.frequencies
   
    def getFrequencyOf(self, depth):
        return self.frequencies[depth]

    def len(self):
        return len(self.frequencies)
    
    def print2(self):
       for i in xrange(len(self.frequencies)):
         if self.frequencies[i] != 0:
           print i, ":", self.frequencies[i]

class LocationSignature(object):
    
    def __init__(self, len):
        self.length = len
        self.distances = {}
        for i in xrange(len):
            self.distances[i] = None
        self.dict_index = 0

    def updateDistance(self, angle, distance):
        self.distances[self.dict_index] = (angle, distance)
        self.dict_index += 1

    def getDistance(self, index):
        return self.distances[index]

    def setDistances(self, distances):
        self.distances = distances

    def getDistances(self):
        return self.distances
    
    def len(self):
        return self.length

def readGBFile(fileName):
    dic = {}
    with open(fileName+".gb", 'r') as GBFile:
        for line in GBFile.readlines():
            line = line.replace('\n', '')
            (key, value) = line.split(',',1)
	    if fileName[0] == 'l':
	        if value == None:
		  continue
		value = value.replace('(','').replace(')','').replace(' ','')
	        (angle, depth) = value.split(',')
                dic[int(key)] = (int(float(angle)), int(depth))
            else:
	    	dic[int(key)] = int(value)
    return dic

def writeGBFile(fileName, dic):
    with open(fileName+".gb", 'w+') as GBFile:
        for key in dic:
            GBFile.write(str(key))
            GBFile.write(',')
            GBFile.write(str(dic[key]))
            GBFile.write('\n')
        
    
if __name__ == "__main__":
    print robo_name
    mode = None
    while mode != "d" and mode != "p":
      mode = raw_input("Enter mode (prepare as p/deploy as d): ")
    
    if mode == "p":
        for location in locations:
            print "Please put Guybrush at point", location, "and press Enter"
            dummy_variable_because_irina_doesnt_like_asdf_as_a_variable_name = raw_input()
            sonar_readings, sonar_intervals = sonar_spin()
            ####TODO change above when using the real code
	   
	    print sonar_readings
	    print len(sonar_readings)
            #Create Location Signature
            location_signature = LocationSignature(len(sonar_readings))
            for i in xrange(len(sonar_readings)):
                location_signature.updateDistance(sonar_intervals[i], sonar_readings[i])
            
            sigFileName = "loc_sig_" + str(location)
            writeGBFile(sigFileName, location_signature.getDistances())
            #also store in dictionary just for the lolz
            loc_sigs[location] = location_signature
            #####
            
            #Create Depth Histogram
            depth_histogram = DepthHistogram()
            for distance in sonar_readings:
              depth_histogram.updateFreq(distance)
                
            histFileName = "dep_his_" + str(location)
            writeGBFile(histFileName, depth_histogram.getFrequencies())
            
	    #also store in dictionary just for the lolz
            dep_hists[location] = depth_histogram
            #####
            depth_histogram.print2()

	    print "Spinning robot back.."
	    somo.rotateClockwise(360)
            

    elif mode == "d":
        k = 4 # no of degrees for each interval we measure
        hist = DepthHistogram()
        readings, intervals = sonar_spin() #([255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255], [3.246376811594203, 3.0434782608695654, 3.449275362318841, 3.6521739130434785, 3.0434782608695645, 3.6521739130434803, 3.855072463768117, 3.6521739130434767, 3.6521739130434767, 3.855072463768117, 3.6521739130434767, 3.652173913043484, 3.85507246376811, 3.855072463768117, 3.652173913043484, 3.6521739130434767, 3.855072463768117, 3.6521739130434767, 3.85507246376811, 3.652173913043484, 3.652173913043484, 3.85507246376811, 3.652173913043484, 3.85507246376811, 3.0434782608695627, 3.855072463768124, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.855072463768124, 3.652173913043484, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.85507246376811, 3.652173913043498, 3.6521739130434696, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.652173913043498, 3.6521739130434696, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.652173913043498, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.6521739130434696, 3.855072463768124, 3.855072463768124, 3.855072463768124, 3.6521739130434696, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.855072463768124, 3.6521739130434696, 3.652173913043498, 3.855072463768124, 3.652173913043441, 3.652173913043498, 3.855072463768124, 3.652173913043441, 3.652173913043498, 3.855072463768124, 3.652173913043498, 3.652173913043441, 3.855072463768124, 3.652173913043498, 3.652173913043441, 3.855072463768124, 3.652173913043498, 3.652173913043498, 3.652173913043441, 3.855072463768124, 3.855072463768124, 3.652173913043498, 3.652173913043441, 3.855072463768124, 3.652173913043498, 3.652173913043441, 3.855072463768124, 3.652173913043498, 3.855072463768124, 3.652173913043498])
	loc = LocationSignature(len(readings))
        histograms_no = 5 #todo
        given_histograms = []
        signature_filenames = []
        
        waypoint_no = [1,2,4,5,7]
        # read the histogram files in memory
        for i in waypoint_no:
          h = DepthHistogram()
          dict = readGBFile("dep_his_"+str(i))
          h.setFrequenciesFromDict(dict)
          given_histograms.append(h)
          signature_filenames.append("loc_sig_"+str(i))

        # create a histogram of the current readings
        for i in xrange(len(readings)):
          hist.updateFreq(readings[i])
        
	# compare it with all other histograms
        sums = [0,0,0,0,0] # must have a fixed number of 5 histograms
        min_sum = 255 * 1000 # Way higher than we would possibly get
        min_index = -1
        for i in xrange(len(given_histograms)):
          for j in xrange(hist.len()):
            sums[i] += (hist.getFrequencyOf(j) - given_histograms[i].getFrequencyOf(j)) ** 2
          if min_sum > sums[i]:
            min_sum = sums[i]
            min_index = i

        print sums

        print "Robot is at position", waypoint_no[min_index]

        # robot is at position min_index now
        # we've left to find the angle rotation

        # wreading the learned sig file and putting it in an object
        default_loc_filename = signature_filenames[min_index]
        default_loc = readGBFile(default_loc_filename)
        default_signature = LocationSignature(len(default_loc))
        for i in xrange(len(default_loc)):
	  default_signature.updateDistance(default_loc[i][0], default_loc[i][1])

        # reading the current sonar readings and putting it in an object
        curr_signature = LocationSignature(len(readings))
        for i in xrange(len(readings)):
	  curr_signature.updateDistance(intervals[i], readings[i])

    	# now we need to interpolate the new readings
	def georgeTrick(distances, i, interval):
	  return distances[i*interval:(i+1)*interval]
			
	new_dist_len = gcd(len(default_signature.distances),len(curr_signature.distances))
        print default_signature.distances	
	new_dic = {}
	for i in range(new_dist_len):
	  interpolation = georgeTrick(map(lambda x: x[1], default_signature.distances.values()), i, len(default_signature.distances)/new_dist_len)
	  new_dic[i] = (i*(360/new_dist_len), interpolation)
	  default_signature.distances = new_dic
			
	  new_dic = {}
	for i in range(new_dist_len):
	  new_dic[i] = (i*(360/new_dist_len), georgeTrick(map(lambda x: x[1], list(curr_signature.distances.values())), i, len(curr_signature.distances)/new_dist_len))
	  curr_signature.distances = new_dic
			
        print ">>", default_signature.distances			
        # comparing the two maps to find the angle we're at
    	
    	mini = 255 * 1000 # Way higher than we would possibly get
    	min_angle = 0

        '''
    	for i in xrange(new_dist_len):
    	  cheese_balls = 0
    	  for j in xrange(new_dist_len):
	    print "!!!", new_dist_len
	    print default_signature.distances[0][1]
	    print curr_signature.distances[(j+i) % new_dist_len][1]
            cheese_balls += (default_signature.distances[j][1] - curr_signature.distances[(j+i)%new_dist_len][1]) ** 2
       	  if cheese_balls < mini:
            mini = cheese_balls
            min_angle = i*gcd
	#print min_index, rotation
        '''
	
        '''# comparing the two maps to find the angle we're at
	def_index = 0
        loc_index = 0
        
    	while def_index < len(default_loc):
	  "LL"
	  def_value = default_signature.getDistances()[def_index][1]
	  curr_value = curr_signature.getDistances()[loc_index % loc.len()][1]
          if math.fabs(def_value - curr_value) > 3:
            loc_index+=1
          else:
            def_index+=1
            loc_index+=1
    
        rotation = k * (loc_index % loc.len())
        #print min_index, rotation
        '''
        
        # Rotation stuff
        dlen = default_signature.len()
	clen = curr_signature.len()
        min_length = min(dlen, clen)
	
	sums = []
	min_sum = 999999
	min_index = -1
	for i in xrange(min_length):
	  sums.append(0)
	  sums[i] = 0
	  for j in xrange(min_length):
	    sums[i] += (default_signature.getDistance(0)[1][j] - curr_signature.getDistance(0)[1][(j + i) % min_length] ** 2)

	  if sums[i] < min_sum:
	    min_sum = sums[i]
	    min_index = i
	
	print "Min index::", i

	somo.rotateClockwise(360)

    else:
        print "Please input argument prepare/deploy"
