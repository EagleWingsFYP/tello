from djitellopy import Tello
import time
from config.settings import FRAME_SIZE, MAX_DISTANCE, debug


class TSCHelper:
    @staticmethod
    def map_axis(x_axis: float, y_axis: float, z_axis: float, mx=FRAME_SIZE[0], my=FRAME_SIZE[1], mz=MAX_DISTANCE*2):
        return \
            x_axis / mx, \
            y_axis / my, \
            z_axis / mz

    @staticmethod
    def calculate_speed(value, map_value, low, high, scale):
        direction = -1 if value < 0 else 1
        speed = max(
            low, 
            min(high, abs(value) * scale)
        )
        return int(map_value * speed * direction)


class TelloControllerBasic:


    TIMEOUT = 1
    MIN_UPDATE_INTERVAL = 0.1



    def __init__(self, tello: Tello, auto_start=True):
        self.tello = tello
        self.is_loop_enabled = True
        self.is_changing_course = False
        self.is_stopped = True

        self.last_move_time = 0
        self.move_deadline = time.time() + self.TIMEOUT

        if auto_start:
            self.start()

    def start(self):
        print("[DBG] TelloBasic: Taking Off.")
        self.tello.connect()
        self.tello.takeoff()

    def stop(self, immediately=False):
        if immediately:
            self.tello.send_rc_control(0, 0, 0, 0)
            self.is_stopped = True
            if debug:
                print("[DBG] Immediate stop command issued.")
        else:
            self.is_stopped = True


    def  enable_loop(self): self.is_loop_enabled = True
    def disable_loop(self): self.is_loop_enabled = False

    
    def move(self, x_axis, y_axis, z_axis, travel=20):

        current_time = time.time()

        if current_time - self.last_move_time < self.MIN_UPDATE_INTERVAL: return False
        
        self.last_move_time = current_time

        if x_axis == 0 and y_axis == 0 and z_axis == 0:
            self.stop(True)
            return True

        if x_axis < 0:   self.tello.move_left(travel)
        elif x_axis > 0: self.tello.move_right(travel)

        if y_axis < 0:   self.tello.move_back(travel)
        elif y_axis > 0: self.tello.move_forward(travel)

        if z_axis < 0:   self.tello.move_down(travel)
        elif z_axis > 0: self.tello.move_up(travel)

        self.move_deadline = current_time + self.TIMEOUT
        self.is_stopped = False
        return False


    def loop(self):

        if not self.is_loop_enabled: return

        if time.time() > self.move_deadline and not self.is_stopped:
            if debug: print("[DBG] TelloBasic: Timeout.")
            self.stop(True)
