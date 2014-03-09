#!/usr/bin/python

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
        readings, intervals = sonar_spin()
        print readings
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
        min = 255 * 1000 # Way higher than we would possibly get
        min_index = -1
        for i in xrange(len(given_histograms)):
            for j in xrange(hist.len()):
                sums[i] += (hist.getFrequencyOf(j) - given_histograms[i].getFrequencyOf(j)) ** 2
            if min > sums[i]:
                min = sums[i]
                min_index = i

        print sums

        print "Robot is at position", waypoint_no[min_index]

        # robot is at position min_index now
        # we've left to find the angle rotation

        # reading the learned sig file and putting it in an object
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


        # comparing the two maps to find the angle we're at
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

	somo.rotateClockwise(360)

    else:
        print "Please input argument prepare/deploy"
