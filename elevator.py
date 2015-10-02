import time

def wait(seconds, reason):
	print("%s (%d seconds)" % (reason, seconds))
	time.sleep(seconds)
	
class Elevator(object):
	def __init__(self):
		self.current_floor = 1
		self.is_open = False
		
	def openDoor(self):
		wait(2, "Opening door")
		self.is_open = True
		
	def closeDoor(self):
		wait(2, "Closing door")
		self.is_open = False
		
	def goToFloor(self, target_floor):
		# assume 2 seconds to move from one floor to the next, but 2 extra seconds to start and 3 extra seconds to stop
		original_floor = self.current_floor
		while (self.current_floor != target_floor):
			# Going up!
			if (self.current_floor < target_floor):
				if (self.current_floor == original_floor):
					wait(2, "Starting elevator")
				wait(2, "Moving from floor %d to %d" % (self.current_floor, self.current_floor + 1))
				if (self.current_floor == target_floor - 1):
					wait(3, "Stopping elevator")
				self.current_floor += 1
			# Going down!
			elif (self.current_floor > target_floor):
				if (self.current_floor == original_floor):
					wait(2, "Starting elevator")
				wait(2, "Moving from floor %d to %d" % (self.current_floor, self.current_floor - 1))
				if (self.current_floor == target_floor + 1):
					wait(3, "Stopping elevator")
				self.current_floor -= 1
				