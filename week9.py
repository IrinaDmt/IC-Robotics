#import stuff

robo_name = '''
 _______               __                      __    
|     __|.--.--.--.--.|  |--.----.--.--.-----.|  |--.
|    |  ||  |  |  |  ||  _  |   _|  |  |__ --||     |
|_______||_____|___  ||_____|__| |_____|_____||__|__|
               |_____|'''
loc_sigs = {1:None, 2:None, 4:None, 5:None, 7:None}
SONAR_STEP = 3

class DepthHistogram(Object):
	
	def __init__(self):
		self.frequencies = {}
		for i in xrange(256):
			self.frequencies[i] = 0
	
	def updateFreq(self, depth):
		self.frequencies[depth] += 1
	
	def getFrequencies(self):
		return self.frequencies
    
class LocationSignature(Object):
    
    def __init__(self):
        self.distances = {}
        for i in xrange(0, 360, SONAR_STEP):
            self.distances[i] = None
            
    def updateDistance(self, angle, distance):
        self.distances[angle] = distance
    
    def getDistances(self):
        return self.distances
    
if __name__ == "__main__":
    print robo_name
    mode = None
    while mode != "deploy" and mode != "prepare":
        mode = raw_input("Enter mode (prepare/deploy): ")
    
    if mode == "prepare":
        for loc_sig in loc_sigs:
            print "Please put Guybrush at point", loc_sig, "and press Enter"
            dummy_variable = raw_input()
            

    elif mode == "deploy":
        pass
    else:
        print "Please input argument prepare/deploy"