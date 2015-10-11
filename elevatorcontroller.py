from elevator import Elevator
from threading import Thread

class ElevatorController(object):
	"""Manages/controls one or more elevators that work together, assuming they both can access the same floors"""

	def __init__(self, elevators, floors):
		"""Creates a elevator controller containing `elevators` (positive int) elevators that can access `floors` (positive int)"""
		self.floors = floors
		self.elevators = list()
		for x in range(elevators):
			self.elevators.append(Elevator(self.floors))
		self.called = dict()  # {1: {"up": False, "down": False}, 2: {"up": False, "down": False}}
		for x in range(floors):
			self.called[x+1] = {"up": False, "down": False}

	def assign_elevator(self):
		"""Monitors elevator calls and assigns an elevator that is either not busy or is able to service the call"""
		while True:
			for elevator in self.elevators:
				if elevator.busy:
					if elevator.going_up:
						for floor in range(elevator.current_floor+1, self.floors+1):
							if self.called[floor]["up"]:
								elevator.go_to[floor] = True
								self.called[floor]["up"] = False
					else:
						for floor in range(elevator.current_floor-1, 0, -1):
							if self.called[floor]["down"]:
								elevator.go_to[floor] = True
								self.called[floor]["down"] = False
				else:
					now_busy = False
					for floor in range(1, self.floors+1):
						if self.called[floor]["up"]:
							elevator.go_to[floor] = True
							self.called[floor]["up"] = False
							now_busy = True
							break
					if now_busy:
						break
					for floor in range(self.floors, 0, -1):
						if self.called[floor]["down"]:
							elevator.go_to[floor] = True
							self.called[floor]["down"] = False
							# now_busy = True
							break

	def call_elevator(self, floor, direction):
		"""Calls an elevator from floor `floor` to the given direction ("up"/"down")"""
		self.called[floor][direction] = True

	def run(self):
		# Start the elevators
		for elevator in self.elevators:
			Thread(target=elevator.run).start()
		# Start the elevator assigner
		Thread(target=self.assign_elevator).start()