from BrickPi import *
import math, sys, random, help_util

class Robot(Object):
	
	#Robots Constructor
	def __init__(self, name="Guybrush Threepwood", length=30, axle=15, speed_left=200, speed_right=204, wheel_radius=2.2, safe_distance=30):
		self.name = name
		self.LENGTH = length
		self.AXLE_DIAMETER = axle
		self.SPEED_LEFT = speed_left
		self.SPEED_RIGHT = speed_right
		self.WHEEL_RADIUS = wheel_radius
		self.SAFE_DISTANCE = safe_distance
		self.sensors = {}
		
		#Setup sensors
		left = self.sensors['LEFT_BUMPER'] = PORT_1
		right = self.sensors['RIGHT_BUMPER'] = PORT_2
		sonar = self.sensors['SONAR'] = PORT_3
		BrickPi.SensorType[left] = TYPE_SENSOR_TOUCH
		BrickPi.SensorType[right] = TYPE_SENSOR_TOUCH
		BrickPi.SensorType[sonar] = TYPE_SENSOR_ULTRASONIC_CONT
		
		# Setup the serial port for communication
		BrickPiSetup()
		
		#Define robot's properties
		self.motor1 = PORT_A
		self.motor2 = PORT_B
		
		BrickPi.MotorEnable[motor1] = 1 #Enable the Motor A
		BrickPi.MotorEnable[motor2] = 1 #Enable the Motor B
		
		#Send the properties of sensors to BrickPi
		BrickPiSetupSensors()
		
		menu()
	
###############################################################	
	
	def menu(self):
		while True:
			# -- making it cool
			print
			sys.stdout.write('+')
			for i in self.name:
				sys.stdout.write('-+')
			print
			sys.stdout.write('|')
			for i in self.name:
				sys.stdout.write('%s|' %(i))
			print
			sys.stdout.write('+')
			for i in self.name:
				sys.stdout.write('-+')
			print
			# --
			
			#Menu
			print "1 - Freeride"
			print "2 - Square"
			print "3 - Bumper Attack"
			print "4 - Keeping Safe Distance"
			print "5 - Wall Following"
			options = {0: freeride, 1: square, 3: bumperAttack, 4: keepingSafeDist, 5: wallFollow}
			option = input("Please choose from the menu: ")
			options[option]()

###############################################################

	def freeride(self):
		input = raw_input(">")
		while (input != ""):
  		if input == "s":
    		dist = raw_input("distance in cm>")
    		if dist == "":
      		dist = 20 
				back(float(dist))
    		stop()
  		elif input == "w":
    		dist = raw_input("distance in cm>")
    		if dist == "":
      		dist = 20
    		fwd(float(dist))
    		stop()
  		elif input == "a":
    		angle = raw_input("angle>")
    		left(float(angle))
    		stop()
  		elif input == "d":
    		angle = raw_input("angle>")
    		right(float(angle))
    		stop()
  		elif input == "square" or input == "sq":
    		size = raw_input("size>")
				if size == "":
					size = 15
    		for i in range(4):
      		fwd(float(size))
      		stop()
      		left90deg()
      		stop()
  		elif input == "stop" or input == "exit":
    		break
  		input = raw_input(">")	
	
###############################################################
	
	def square(self):
		size = raw_input("size (in cm): ")
		if size == "":
			size = 15
		for i in range(4):
			fwd(float(size))
			stop()
			left90deg()
			stop()
	
###############################################################
	
	def bumperAttack(self):
		while True:
			result = BrickPiUpdateValues()
			if not result:
				if BrickPi.Sensor[LEFT_BUMPER] and BrickPi.Sensor[RIGHT_BUMPER]:
					print "Front Collision"
					back(ROBOT_LENGTH) #back ROBOT_LENGTH cm
					choice = random.choice(["left", "right"]) #randomly choose left or right
					if choice is "left":
						left(60)
						fwd(AXLE_DIAMETER)
						right(60)
					elif choice is "right":
						right(60)
						fwd(AXLE_DIAMETER)
						left(60)
					fwd(1) #continue going forward (return to loop)
				elif BrickPi.Sensor[RIGHT_BUMPER]:
					print "Right Collision"
					back(ROBOT_LENGTH) #back ROBOT_LENGTH cm
					left(60) #turn left 90 degrees
					fwd(AXLE_DIAMETER) #forward AXLE_DIAMETER cm
					right(60) #turn right 90 degrees
					fwd(1) #return to loop
				elif BrickPi.Sensor[LEFT_BUMPER]:
					print "Left Collision"
					back(ROBOT_LENGTH) #back ROBOT_LENGTH cm
					right(60) #turn right 90 degrees
					fwd(AXLE_DIAMETER) #forward AXLE_DIAMETER cm
					left(60) #turn left 90 degrees
					fwd(1) #return to loop
				else:
					fwd(1) #continue

###############################################################

	def keepingSafeDist(self):
		distance_measurements = []
 
		while len (distance_measurements) < 9: #should be odd if integer results are desired
			result = BrickPiUpdateValues()
			if not result:
				distance_measurements.insert(0, BrickPi.Sensor[SONAR])
 
		while True:
			result = BrickPiUpdateValues()
			if not result:
				#calculate median distance over last 10 results
				distance_measurements.pop()
				distance_measurements.insert(0, BrickPi.Sensor[SONAR])
				distance = help_util.median(distance_measurements)
				if distance > DESIRED_DISTANCE:
					print "too far away"
					#set 'proportional gain' speed
				elif distance < DESIRED_DISTANCE:
					print "too close"
					#set 'proportional gain speed backwards
				else:
					print "correct distance"
					#stop

###############################################################

	#Timer
	def timer(no_seconds):
		ot = time.time()
		while(time.time() - ot < no_seconds):	#running while loop for
  																				#no_seconds seconds
			BrickPiUpdateValues()            		# Ask BrickPi to update values
    																			#for sensors/motors
			time.sleep(.1)                 		  # sleep for 100 ms







