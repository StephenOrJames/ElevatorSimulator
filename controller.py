from elevator import Elevator
from threading import Thread

class Controller(object):
	"""Manages/controls one or more elevators that work together, assuming they both can access the same floors"""

	def __init__(self, elevators, floors):
		"""Creates a elevator controller containing `elevators` (positive int) elevators that can access `floors` (positive int)"""
		self.floors = floors
		self.elevators = list()
		for x in range(elevators):
			self.elevators.append(Elevator(self.floors, name="Elevator " + str(x+1)))
		self.called = dict()  # {1: {"up": False, "down": False}, 2: {"up": False, "down": False}}
		for x in range(floors):
			self.called[x+1] = {"up": False, "down": False}

	def monitor_calls(self):
		"""Monitors elevator calls"""
		while True:
			for floor in range(1, self.floors+1):
				for direction in ["up", "down"]:
					if self.called[floor][direction]:
						self.assign_elevator(floor, direction)

	def assign_elevator(self, floor, direction):
		"""Assigns an elevator that is either not busy or is able to service the call"""
		assigned = None
		elevators = sorted(self.elevators, key=lambda e: abs(e.current_floor - floor))
		for elevator in elevators:
			if elevator.busy:
				# called to go up and elevator going up from lower floor
				if (direction == "up") and elevator.going_up and (elevator.current_floor < floor):
					elevator.go_to[floor] = True
					self.called[floor][direction] = False
					break
				# called to go down and elevator going down from higher floor
				elif (direction == "down") and not elevator.going_up and (elevator.current_floor > floor):
					elevator.go_to[floor] = True
					self.called[floor][direction] = False
					break
			else:
				# elevator has nothing to do, so give it something to do
				elevator.busy = True
				elevator.go_to[floor] = True
				self.called[floor][direction] = False
				break

	def call_elevator(self, floor, direction):
		"""Calls an elevator from floor `floor` to the given direction ("up"/"down")"""
		self.called[floor][direction] = True

	def run(self):
		# Start the elevators
		for elevator in self.elevators:
			Thread(target=elevator.run).start()
		# Start the elevator assigner
		Thread(target=self.monitor_calls).start()
