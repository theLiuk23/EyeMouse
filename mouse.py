from screeninfo import get_monitors
from eyes import Eyes
import pyautogui
import sys, time


class Mouse:
    def __init__(self, MOUSE_SMOOTHNESS):
        self.eyes = Eyes()
        pyautogui.FAILSAFE = False
        self.MOUSE_SMOOTHNESS = MOUSE_SMOOTHNESS
        self.MAX_L_DISTANCE = None
        self.MAX_R_DISTANCE = None
        self.MIN_DISTANCE = None
        self.screen_size = self.get_screen_size()
        
    
    def calibrate(self, frame):
        # print("Watch the left border of your screen")
        # time.sleep(5)
        # l_distance = self.eyes.detect_eyes_distance(frame)
        # if not l_distance:
        #     sys.exit(1)
        # self.MAX_L_DISTANCE = 1/l_distance

        # print("Watch the right border of your screen")
        # time.sleep(5)
        # r_distance = self.eyes.detect_eyes_distance(frame)
        # if not r_distance:
        #     sys.exit(1)
        # self.MAX_R_DISTANCE = 1/r_distance

        # print("Watch the center of your screen")
        # time.sleep(5)
        # center = self.eyes.detect_eyes_distance(frame)
        # if not center:
        #     sys.exit(1)
        # self.MIN_DISTANCE = 1/center

        # print(f'MIN: {self.MIN_DISTANCE};   MAX: {self.MAX_R_DISTANCE}, {self.MAX_L_DISTANCE}')
        self.MAX_L_DISTANCE = -14
        self.MAX_R_DISTANCE = 14
        self.MIN_DISTANCE = 7


    # distance is a float value that determines the distance between the pupils
    # if distance is positive, the user rotated to the right
    # if distance is negative, to the left
    def move_mouse(self, distance: float):
        if None in [self.MAX_L_DISTANCE, self.MAX_R_DISTANCE, self.MIN_DISTANCE]:
            print("You need to calibrate before using the program!")
            sys.exit(1)

        if distance < 0:
            prop = (distance + self.MIN_DISTANCE) / (self.MAX_L_DISTANCE - self.MIN_DISTANCE)
            print(f'{distance} + {self.MIN_DISTANCE}) / ({self.MAX_L_DISTANCE} - {self.MIN_DISTANCE}')
        else:
            prop = (distance - self.MIN_DISTANCE) / (self.MAX_R_DISTANCE - self.MIN_DISTANCE)
            print(f'{distance} - {self.MIN_DISTANCE}) / ({self.MAX_L_DISTANCE} - {self.MIN_DISTANCE}')
        movement = self.screen_size[0] / 2 + (prop * self.screen_size[0] / 2)

        if movement > self.screen_size[0]:
            movement = self.screen_size[0]

        if movement < 0:
            movement = 0

        # print("DISTANCE:", distance, "PROP:", prop, "MOVEMENT:", movement)
        pyautogui.moveTo(movement, 520, 1/self.MOUSE_SMOOTHNESS)


    def get_screen_size(self, width_is_fixed: bool = False) -> tuple[int]:
        w, h = 0, 0
        for monitor in get_monitors():
            if width_is_fixed:
                w = monitor.width
                h += monitor.height
            else:
                w += monitor.width
                h = monitor.height
        return (w, h)