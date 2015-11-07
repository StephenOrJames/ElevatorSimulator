import time

class Elevator(object):
	
	def __init__(self, floors, name=""):
		"""Initialize the state of the elevator"""
		if name != "":
			self.name = name
		else:
			self.name = "Elevator"
		self.current_floor = 1
		self.top_floor = floors
		self.busy = False  # if the elevator is busy
		self.door_open = False  # if the door is open
		self.going_up = True  # if the elevator is (or was last) going up
		self.go_to = dict()  # status of floors to be visited by elevator
		for x in range(floors):
			self.go_to[x+1] = False

	def __str__(self):
		return self.name

	def do(self, seconds, action):
		"""Waits for a period of seconds to simulate an action being carried out"""
		#print("%s (%d seconds)" % (action, seconds))
		#print(self.get_status())
		time.sleep(seconds)

	def get_status(self):
		go_to = list()
		for x in self.go_to.keys():
			if self.go_to[x]:
				go_to.append(x)
		return "%(name)s (floor: %(floor)02d, door: %(door)s, direction: %(direction)s, go to: %(go_to)s)" % {
			"name": self.name,
			"floor": self.current_floor,
			"door": "open" if self.door_open else "closed",
			"direction": "up" if self.going_up else "down",
			"go_to": repr(go_to)
		}

	def open_door(self):
		"""Opens the elevator's door"""
		if not self.door_open:
			self.do(2, "Opening door")
			self.door_open = True

	def close_door(self):
		"""Closes the elevator's door"""
		if self.door_open:
			self.do(2, "Closing door")
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
					self.do(1, "Starting elevator")
				self.do(2, "Moving from floor %d to %d" % (self.current_floor, self.current_floor + 1))
				self.current_floor += 1
				if (self.current_floor == target_floor):
					self.do(3, "Stopping elevator")
			# Going down!
			elif (self.current_floor > target_floor):
				self.going_up = False
				if (self.current_floor == original_floor):
					self.do(1, "Starting elevator")
				self.do(2, "Moving from floor %d to %d" % (self.current_floor, self.current_floor - 1))
				self.current_floor -= 1
				if (self.current_floor == target_floor):
					self.do(3, "Stopping elevator")

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
				self.do(5, "Loading/unloading elevator")
				self.close_door()
