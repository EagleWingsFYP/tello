
import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from core.util.classes.TelloDummy import TelloDummy as Tello


class DummyController:


    def __init__(self, auto_start=True):
        self.tello = Tello()
        self.tello.streamon()
        self.travel = 20

        if auto_start:
            self.start()

    def start(self):
        self.tello.connect()
        self.tello.takeoff()
        pass

    def set_travel(self, travel):
        self.travel=travel

    
    def stop(self, immediately=True):
        self.tello.stop()
        pass


    def  enable_loop(self): pass
    def disable_loop(self): pass
    

    def move(self, x_axis, y_axis, z_axis, travel=20):
        self.set_travel(travel)
        
        if x_axis == 0 and y_axis == 0 and z_axis == 0:
            self.tello.stop()
            return

        if x_axis < 0:   self.tello.move_left(self.travel)
        elif x_axis > 0: self.tello.move_right(self.travel)

        if y_axis < 0:   self.tello.move_back(self.travel)
        elif y_axis > 0: self.tello.move_forward(self.travel)

        if z_axis < 0:   self.tello.move_down(self.travel)
        elif z_axis > 0: self.tello.move_up(self.travel)


    def loop(self):
        pass