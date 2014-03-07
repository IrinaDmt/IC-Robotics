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
    
    def getFrequencies(self):
        return self.frequencies
    
    def len(self):
        return len(self.frequencies)
    
class LocationSignature(object):
    
    def __init__(self):
        self.distances = {}
        for i in xrange(0, 360, SONAR_STEP):
            self.distances[i] = None
            
    def updateDistance(self, angle, distance):
        self.distances[angle] = distance
    
    def getDistances(self):
        return self.distances
    
    def len(self):
        return len(self.distances)
    
def readGBFile(fileName):
    dic = {}
    with open(fileName+".gb", 'r') as GBFile:
        for line in GBFile.readlines():
            line = line.replace('\n', '')
            (key, value) = line.split(',')
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
    #while mode != "deploy" and mode != "prepare":
    #    mode = raw_input("Enter mode (prepare/deploy): ")
    
    mode = "prepare"
    
    if mode == "prepare":
        for location in locations:
            print "Please put Guybrush at point", location, "and press Enter"
            dummy_variable_because_irina_doesnt_like_asdf_as_a_variable_name = raw_input()
            sonar_readings = sonar_spin_left()
            
            #Create Location Signature
            location_signature = LocationSignature()
            for (distance_index, angle) in enumerate(range(0, 360, SONAR_STEP)):
                location_signature.updateDistance(angle, sonar_readings[distance_index])
            
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
            

    elif mode == "deploy":
        k = 4 # no of degrees for each interval we measure
        hist = DepthHistogram()
        loc = LocationSignature()
        readings = sonar_spin()
        histograms_no = 5 #todo
            
        # create a histogram of the current readings
        for i in xrange(len(readings)):
            hist.updateFreq(readings[i])

        # compare it with all other histograms
        sums = []
        min = 1000
        min_index = -1
        for i in xrange(histograms_no):
            for j in xrange(hist.len()):
                sums[i] += (hist[j] - given_histogram[i][j]) ** 2
            if min > sums[i]:
                min = sums[i]
                min_index = i
    
        # robot is at position min_index now
        # we've left to find the angle rotation
        default_loc = getLocationSignature(min_index)
        def_index = 0 
        loc_index = 0 
        while def_index < default_loc.len():
            if math.fabs(default_loc[def_index], loc[loc_index % loc.len()]) > 3:
                loc_index+=1
            else:
                def_index+=1
                loc_index+=1
    
        rotation = k * (loc_index % loc.len())
        print min_index, rotation    

    else:
        print "Please input argument prepare/deploy"