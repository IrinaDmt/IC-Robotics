from BrickPi import *
import math

class Robot(Object):
	
	#Robots Constructor
	def __init__(self, name="Guybrush Threepwood" length=30, axle=15, speed_left=200, speed_right=204, wheel_radius=2.2, safe_distance=30):
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
	
	def menu(self):
		while True:
			# -- making it cool
			print "+",
			for i in self.name:
				print "-+",
			print
			print "|",
			for i in self.name:
				print "%s|" % (i),
			print
			print "+",
			for i in self.name:
				print "-+",
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

	def freeride(self):
		#TODO: Paste that shitty RC program thingy
	
	def suare(self):
		size = raw_input("size (in cm): ")
    if size == "":
      size = 15
    for i in range(4):
      fwd(float(size))
      stop()
      left90deg()
      stop()
	
	
	
	
	def bumperAttack(self):
		while True:
			result = BrickPiUpdateValues()
			if not result:
				if BrickPi.Sensor[LEFT_BUMPER] and BrickPi.Sensor[RIGHT_BUMPER]:
					print "Front Collision"
      		back(ROBOT_LENGTH) #back ROBOT_LENGTH cm
					choice = "left" #randomly choose left or right
					if choice is "left":
						left(90)
						fwd(AXLE_DIAMETER)
						right(90)
					elif choice is "right":
						right(90)
						fwd(AXLE_DIAMETER)
						left(90)
					fwd(1) #continue going forward (return to loop)
				elif BrickPi.Sensor[RIGHT_BUMPER]:
					print "Right Collision"
					back(ROBOT_LENGTH) #back ROBOT_LENGTH cm
					left(90) #turn left 90 degrees
					fwd(AXLE_DIAMETER) #forward AXLE_DIAMETER cm
					right(90) #turn right 90 degrees
					fwd(1) #return to loop
				elif BrickPi.Sensor[LEFT_BUMPER]:
					print "Left Collision"
					back(ROBOT_LENGTH) #back ROBOT_LENGTH cm
					right(90) #turn right 90 degrees
					fwd(AXLE_DIAMETER) #forward AXLE_DIAMETER cm
					left(90) #turn left 90 degrees
					fwd(1) #return to loop
				else:
					fwd(1) #continue
      
      sinexise pou dame
      
      
	#Sets the speed of the left motor
	def setSpeedLeft(self, speed):
		self.speed_left = speed
	
	#Sets the speed of the right motor
	def setSpeedRight(self, speed):
		self.speed_right = speed
	
	#Updates the speed
	def updateSpeed(self, no_seconds):
		BrickPi.MotorSpeed[motor1] = speed_left
		BrickPi.MotorSpeed[motor2] = speed_right
		timer(no_seconds)

	#Timer
	def timer(no_seconds):
		ot = time.time()
		while(time.time() - ot < no_seconds):    #running while loop for
  																				#no_seconds seconds
			BrickPiUpdateValues()            # Ask BrickPi to update values
    																#for sensors/motors
			time.sleep(.1)                   # sleep for 100 ms
	
	#Goes forward
	def fwd(self, centimeters, speed_left = self.speed_left,  speed_right = self.speed_right):
		self.speed_left = speed_left
		self.speed_right = speed_right
		no_seconds = getSecFromDist(centimeters)
		updateSpeed(no_seconds)
	
	#Goes backwards
	def bwd(self, centimeters, speed_left = self.speed_left,  speed_right = self.speed_right):
		self.speed_left = -speed_left
		self.speed_right = -speed_right
		no_seconds = getSecFromDist(centimeters)
		updateSpeed(no_seconds)
	
	#TODO
	def getSecFromDist(self, centimeters):
		pass
	
	def turnLeft(self, angle, x):
		self.turn_speed_left = - abs(1.0 * self.speed_left / x)
		self.turn_speed_right = abs(1.0 * self.speed_right / x)
		no_seconds = getSecFromAngle(angle)
		updateSpeed(no_seconds)
	
	def turnRight(self, angle, x):
		self.turn_speed_left = abs(1.0 * self.speed_left / x)
		self.turn_speed_right = - abs(1.0 * self.speed_right / x)
		no_seconds = getSecFromAngle(angle)
		updateSpeed(no_seconds)
	
	#TODO
	def getSecFromAngle(self, angle):
		pass
	
	
	
	
		
		
		
		
		
		
		
