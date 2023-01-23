from screeninfo import get_monitors
from eyes import Eyes
import pyautogui


class Mouse:
    def __init__(self, MOUSE_SMOOTHNESS):
        self.MOUSE_SMOOTHNESS = MOUSE_SMOOTHNESS
        self.PRECISION = 3 # max possible delta (delta value if you move your pupil to the edge of the eye)
        self.MAX_MOVEMENT = 50 # max number of pixel the pointer will move in one frame
        self.MAX_ACCELERATION = 0.1 # min and max prevent mouse flickering or crazy movement
        self.MIN_ACCELERATION = 0.01
        self.old_point = None
        self.screen_size = self.get_screen_size()
        
    
    def set_initial_point(self, initial_point):
        if initial_point is None:
            return False
        self.old_point = initial_point
        print(f"success: {self.old_point}")
        return True


    def calc_delta(self, new_point) -> tuple[float]:
        if new_point is None or self.old_point is None:
            return (0, 0)
        # print(f'POINTS: {new_point}, {self.old_point}')
        new_x, new_y = new_point
        old_x, old_y = self.old_point
        delta = (new_x - old_x, new_y - old_y)
        # print(f'DELTA: {delta}')
        if abs(delta[0]) < self.MIN_ACCELERATION or abs(delta[1]) < self.MIN_ACCELERATION:
            return (0, 0)
        elif abs(delta[0]) > self.MAX_ACCELERATION or abs(delta[1]) > self.MAX_ACCELERATION:
            return (self.MAX_ACCELERATION, self.MAX_ACCELERATION)
        else:
            return delta


    def move_mouse(self, point: tuple[int]):
        pyautogui.moveTo(point)


    def get_screen_size(self, width_is_fixed:bool = False) -> tuple[int]:
        w, h = 0, 0

        for monitor in get_monitors():
            if width_is_fixed:
                w = monitor.width
                h += monitor.height
            else:
                w += monitor.width
                h = monitor.height

        return (w, h)