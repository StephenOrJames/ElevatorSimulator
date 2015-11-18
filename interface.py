import tkinter as tk


class Interface(object):
    def __init__(self, controller):
        self.controller = controller
        self.floors = controller.floors  # number of floors
        self.window = tk.Tk()
        self.window.title("ElevatorSimulator")
        self.displays = dict()
        self.displays[0] = dict()
        self.displays[0]["frame"] = tk.Frame(self.window, highlightbackground="black", highlightthickness=1)
        self.displays[0]["frame"].grid(row=0, column=0)
        tk.Label(self.displays[0]["frame"], text="Call Elevator").grid(row=0, column=0, columnspan=2)
        tk.Label(self.displays[0]["frame"], text="Up").grid(row=1, column=0)
        tk.Label(self.displays[0]["frame"], text="Down").grid(row=1, column=1)
        self.displays[0]["calls"] = dict()
        for i in range(1, self.floors + 1):
            self.displays[0]["calls"][i] = dict()
            self.displays[0]["calls"][i]["up"] = tk.Button(
                self.displays[0]["frame"],
                text="%i (up)" % i,
                command=lambda f=i: self.controller.call_elevator(f, "up")
            )
            self.displays[0]["calls"][i]["down"] = tk.Button(
                self.displays[0]["frame"],
                text="%i (down)" % i,
                command=lambda f=i: self.controller.call_elevator(f, "down")
            )
            if i != self.floors:
                self.displays[0]["calls"][i]["up"].grid(row=self.floors + 2 - i, column=0)
            if i != 1:
                self.displays[0]["calls"][i]["down"].grid(row=self.floors + 2 - i, column=1)
        self.update_calls_display(False)
        for i in range(1, len(self.controller.elevators) + 1):
            display = dict()
            display["frame"] = tk.Frame(self.window, highlightbackground="black", highlightthickness=1)
            display["frame"].grid(row=0, column=i)
            display["name"] = tk.Label(display["frame"], text=self.controller.elevators[i - 1].name)
            display["name"].grid(row=0, column=0, columnspan=2)
            display["floor"] = tk.Label(display["frame"])
            display["floor"].grid(row=1, column=0)
            display["dir"] = tk.Label(display["frame"])
            display["dir"].grid(row=1, column=1)
            display["go_to"] = dict()
            for j in range(1, self.floors + 1):
                display["go_to"][j] = tk.Button(display["frame"], text=j, width=3,
                                             command=lambda e=i - 1, f=j: self.send_elevator(e, f))
                display["go_to"][j].grid(row=self.floors + 2 - j, column=0, columnspan=2)
            self.displays[i] = display
            self.update_display(i, False)

    def send_elevator(self, elevator, floor):
        self.controller.elevators[elevator].go_to[floor] = True

    def update_calls_display(self, continuous=True):
        for i in range(1, self.floors + 1):
            self.displays[0]["calls"][i]["up"]["bg"] = "gold" if self.controller.called[i]["up"] else "SystemButtonFace"
            self.displays[0]["calls"][i]["down"]["bg"] = "gold" if self.controller.called[i][
                "down"] else "SystemButtonFace"
        if continuous:
            self.window.after(500, self.update_calls_display)

    def update_display(self, i, continuous=True):
        elevator = self.controller.elevators[i - 1]
        self.displays[i]["floor"]["text"] = elevator.current_floor
        self.displays[i]["dir"]["text"] = "up" if elevator.going_up else "down"
        for j in range(1, self.floors + 1):
            # blue: open; green: current floor; gold: called; otherwise, default color
            if elevator.current_floor == j:
                self.displays[i]["go_to"][j]["bg"] = "blue" if elevator.door_open else "green"
            elif elevator.go_to[j]:
                self.displays[i]["go_to"][j]["bg"] = "gold"
            else:
                self.displays[i]["go_to"][j]["bg"] = "SystemButtonFace"
        if continuous:
            self.window.after(500, lambda d=i: self.update_display(d))

    def update_displays(self):
        self.update_calls_display()
        for i in range(1, len(self.controller.elevators) + 1):
            self.update_display(i)

    def run(self):
        self.window.after(0, self.update_displays)
