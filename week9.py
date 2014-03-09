from motion import *

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

#constants for debugging
init_readings = [255, 255, 255, 255, 255, 255, 255, 36, 35, 37, 35, 33, 32, 33, 32, 33, 34, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 27, 24, 24, 26, 31, 32, 32, 32, 32, 28, 26, 26, 27, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]
init_intervals = [6, 7, 6, 7, 8, 8, 8, 6, 6, 7, 6, 7, 6, 7, 6, 6, 7, 6, 6, 6, 8, 7, 6, 8, 6, 7, 6, 7, 6, 8, 8, 7, 8, 8, 7, 8, 7, 7, 7, 6, 7, 6, 8, 8, 6, 8, 8, 6, 8, 6, 8, 6]

dep_readings = [255, 255, 255, 255, 255, 255, 255, 36, 35, 35, 34, 33, 33, 32, 32, 33, 34, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 33, 34, 34, 27, 25, 24, 24, 24, 23, 23, 24, 26, 28, 28, 27, 28, 28, 28, 28, 28, 28, 28, 28]

dep_intervals = [6, 6, 6, 7, 7, 8, 6, 6, 6, 7, 6, 6, 6, 7, 6, 6, 6, 6, 8, 6, 6, 8, 8, 7, 8, 7, 8, 7, 7, 7, 6, 7, 6, 6, 7, 7, 6, 7, 6, 6, 6, 6, 6, 7, 6, 7, 7, 7, 6, 8, 7, 7, 8, 7]


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
        self.distances = {}
        for i in xrange(len):
            self.distances[i] = None
            
    def updateDistance(self, angle, distance):
        self.distances[i] = (angle, distance)
    
    def getDistances(self):
        return self.distances
    
    def len(self):
        return len(self.distances)
    
def readGBFile(fileName):
    dic = {}
    with open(fileName+".gb", 'r') as GBFile:
        for line in GBFile.readlines():
            line = line.replace('\n', '')
            (key, value) = line.split(',',1)
	    if fileName[0] == 'l':
	    	value = value.replace('(','').replace(')','').replace(' ','')
	    	(angle, depth) = value.split(',')
		dic[int(key)] = (int(angle), int(depth))
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
            sonar_readings = init_readings #sonar_spin_left()
	    sonar_intervals = init_intervals
            ####TODO change above when using the real code
	    
            #Create Location Signature
            location_signature = LocationSignature(len(sonar_readings))
            for i in xrange(len(init_readings)):
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
            

    elif mode == "d":
        k = 4 # no of degrees for each interval we measure
        hist = DepthHistogram()
        readings = dep_readings#sonar_spin()
        loc = LocationSignature(len(readings))
        histograms_no = 1 #todo
        given_histograms = []
	signature_filenames = []

        # read the histogram files in memory
	for i in [1,2,4,5,7]:
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
        min = 1000
        min_index = -1
        for i in xrange(len(given_histograms)):
            for j in xrange(hist.len()):
                sums[i] += (hist.getFrequencyOf(j) - given_histograms[i].getFrequencyOf(j)) ** 2
            if min > sums[i]:
                min = sums[i]
                min_index = i
   
        # robot is at position min_index now
        # we've left to find the angle rotation

        # reading the learned sig file and putting it in an object
        default_loc_filename = signature_filenames[min_index]
        default_loc = readGBFile(default_loc_filename)
		default_signature = LocationSignature(len(default_loc))
		for i in xrange(len(default_loc)):
	    	updateDistance(default_loc[i][0], default_loc[i][1])

        # reading the current sonar readings and putting it in an object
        curr_signature = LocationSignature(len(dep_readings))
        for i in xrange(len(dep_readings)):
			curr_signature.updateDistance(dep_intervals[i], dep_readings[i])

	# now we need to interpolate the new readings


        # comparing the two maps to find the angle we're at
	def_index = 0 
        loc_index = 0 
        
	while def_index < len(default_loc):
            if math.fabs(default_loc[def_index], loc[loc_index % loc.len()]) > 3:
                loc_index+=1
            else:
                def_index+=1
                loc_index+=1
    
        rotation = k * (loc_index % loc.len())
        print min_index, rotation    

    else:
        print "Please input argument prepare/deploy"
