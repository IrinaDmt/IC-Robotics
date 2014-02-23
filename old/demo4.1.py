import motion 
import time
import particles

for i in range(4):
  motion.fwd_amt(50)
  motion.stop()
  motion.turn(90, "r")
  motion.stop()

'''
particles.initialise()
particles.draw()
time.sleep(1)

particles.update_forward(100)
particles.draw()
time.sleep(1)

particles.update_forward(100)
particles.draw()
time.sleep(1)

particles.update_forward(100)
particles.draw()
time.sleep(1)

particles.update_rotate(90)
particles.draw()
time.sleep(1)

particles.update_forward(100)
particles.draw()
time.sleep(1)

particles.update_forward(100)
particles.draw()
time.sleep(1)

particles.update_forward(100)
particles.draw()
time.sleep(1)

particles.update_rotate(90)
particles.draw()
time.sleep(1)

particles.update_forward(100)
particles.draw()
time.sleep(1)

particles.update_forward(100)
particles.draw()
time.sleep(1)

particles.update_forward(100)
particles.draw()
time.sleep(1)'''
