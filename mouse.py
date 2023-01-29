from screeninfo import get_monitors
from eyes import Eyes
import pyautogui
import sys, time


class Mouse:
    def __init__(self, MOUSE_SMOOTHNESS):
        self.eyes = Eyes()
        pyautogui.FAILSAFE = False
        self.MOUSE_SMOOTHNESS = MOUSE_SMOOTHNESS
        self.MAX_DISTANCE = None
        self.MIN_DISTANCE = None
        self.screen_size = self.get_screen_size()
        
    
    def calibrate(self, frame):
        print("Watch the left border of your screen")
        time.sleep(5)
        l_distance = self.eyes.detect_eyes_distance(frame)
        if not l_distance:
            sys.exit(1)

        print("Watch the right border of your screen")
        time.sleep(5)
        r_distance = self.eyes.detect_eyes_distance(frame)
        if not r_distance:
            sys.exit(1)
        self.MAX_DISTANCE = (l_distance + r_distance) / 2

        print("Watch the center of your screen")
        time.sleep(5)
        center = self.eyes.detect_eyes_distance(frame)
        if not center:
            sys.exit(1)
        self.MIN_DISTANCE = center

        print(f'MIN: {self.MIN_DISTANCE};   MAX: {self.MAX_DISTANCE}')
        # self.MAX_L_DISTANCE = -14
        # self.MAX_R_DISTANCE = 14
        # self.MIN_DISTANCE = 7


    # distance is a float value that determines the distance between the pupils
    # if distance is positive, the user rotated to the right
    # if distance is negative, to the left
    def move_mouse(self, distance: float):
        screen_center = self.screen_size[0] / 2 # 1920
        distance = distance + 7 * (distance < 0) - 7 * (distance > 0) # if distance > 0 substract 7 else add 7
        prop = distance / 7
        x_pixel = screen_center + prop * screen_center

        print("DISTANCE:", distance, "PROP:", prop, "MOVEMENT:", x_pixel)
        pyautogui.moveTo(x_pixel, 520, 1/self.MOUSE_SMOOTHNESS)


    def get_screen_size(self, width_is_fixed: bool = False) -> tuple[int]:
        # w, h = 0, 0
        # for monitor in get_monitors():
        #     if width_is_fixed:
        #         w = monitor.width
        #         h += monitor.height
        #     else:
        #         w += monitor.width
        #         h = monitor.height
        # return (w, h)
        return (1920, 1080)