import time
import threading

lock = threading.Lock()

def wait(seconds, reason):
	with lock:
		print("%s (%d seconds)" % (reason, seconds))
	time.sleep(seconds)

class Elevator(object):
	def __init__(self, floors):
		"""Initialize the state of the elevator"""
		self.current_floor = 1
		self.top_floor = floors
		self.busy = False  # if the elevator is busy
		self.door_open = False  # if the door is open
		self.going_up = True  # if the elevator is (or was last) going up
		self.go_to = dict()  # status of floors to be visited by elevator
		for x in range(floors):
			self.go_to[x+1] = False

	def open_door(self):
		"""Opens the elevator's door"""
		if not self.door_open:
			wait(2, "Opening door")
			self.door_open = True

	def close_door(self):
		"""Closes the elevator's door"""
		if self.door_open:
			wait(2, "Closing door")
			self.door_open = False

	def go_to_floor(self, target_floor):
		"""Moves the elevator from its current floor to target_floor"""
		# assume 2 seconds to move from one floor to the next, but 1 extra second to start and 3 extra seconds to stop
		if self.door_open:  # We don't want an elevator moving with open doors
			self.close_door()
		original_floor = self.current_floor
		while (self.current_floor != target_floor):
			# Going up!
			if (self.current_floor < target_floor):
				self.going_up = True
				if (self.current_floor == original_floor):
					wait(1, "Starting elevator")
				wait(2, "Moving from floor %d to %d" % (self.current_floor, self.current_floor + 1))
				if (self.current_floor == target_floor - 1):
					wait(3, "Stopping elevator")
				self.current_floor += 1
			# Going down!
			elif (self.current_floor > target_floor):
				self.going_up = False
				if (self.current_floor == original_floor):
					wait(1, "Starting elevator")
				wait(2, "Moving from floor %d to %d" % (self.current_floor, self.current_floor - 1))
				if (self.current_floor == target_floor + 1):
					wait(3, "Stopping elevator")
				self.current_floor -= 1

	def next_floor_up(self):
		"""Returns the next floor above the current floor to go to or None"""
		for f in range(self.current_floor, self.top_floor+1):
			if self.go_to[f] == True:
				return f
		return None

	def next_floor_down(self):
		"""Returns the next floor below the current floor to go to or None"""
		for f in range(self.current_floor-1, 0, -1):
			if self.go_to[f] == True:
				return f
		return None

	def run(self):
		"""Puts the elevator in operation"""
		while True:
			# Check floors in the direction the elevator is (or was last) going first
			if self.going_up:
				next_floor = self.next_floor_up()
			else:
				next_floor = self.next_floor_down()
			# Check floors in the opposite direction is no floor was received
			if next_floor is None:
				if self.going_up:
					next_floor = self.next_floor_down()
				else:
					next_floor = self.next_floor_up()
			if next_floor is None:
				# No work to do
				self.busy = False
				continue
			else:
				# Work to do
				self.busy = True
				self.go_to_floor(next_floor)
				self.go_to[next_floor] = False
				self.open_door()
				wait(5, "Loading/unloading elevator")
				self.close_door()
