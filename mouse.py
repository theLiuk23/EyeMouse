from screeninfo import get_monitors
from eyes import Eyes
import pyautogui


class Mouse:
    def __init__(self, MOUSE_SMOOTHNESS):
        pyautogui.FAILSAFE = False
        self.MOUSE_SMOOTHNESS = MOUSE_SMOOTHNESS
        self.VERT_MULTIPLIER = 1 # max possible delta (delta value if you move your pupil to the edge of the eye)
        self.HOR_MULTIPLIER = 1 # max possible delta (delta value if you move your pupil to the edge of the eye)
        self.MAX_MOVEMENT = 50 # max number of pixel the pointer will move in one frame
        self.MAX_ACCELERATION = 0.1 # min and max prevent mouse flickering or crazy movement
        self.MIN_ACCELERATION = 0.01
        self.screen_size = self.get_screen_size()
        
    
    def set_initial_point(self, initial_point):
        if initial_point is None:
            return False
        self.old_point = initial_point
        print(f"success: {self.old_point}")
        return True


    def calc_pupil(self, curr_eye: list[tuple[int]], curr_pupil: tuple[int]) -> tuple[float] | None:
        # if self.prev_eye is None or self.prev_pupil is None:
        #     return None
        try:
            x_axis = abs(curr_eye[1].x - curr_eye[0].x)
            y_axis = abs(curr_eye[3].y - curr_eye[2].y)

            x_moved_pupil = curr_pupil.x - curr_eye[0].x
            y_moved_pupil = curr_pupil.y - curr_eye[2].y
            
            x = x_moved_pupil * self.screen_size[0] / x_axis
            y = y_moved_pupil * self.screen_size[1] / y_axis
            
            print(f'POINT: {x, y}')
            return (x, y)
        except:
            return None



    def move_mouse(self, curr_eye: list[tuple[int]], curr_pupil: tuple[int]):
        position = self.calc_pupil(curr_eye, curr_pupil)
        if position is not None:
            x = position[0] * self.HOR_MULTIPLIER
            y = position[1] * self.VERT_MULTIPLIER
            pyautogui.moveTo(x, y, 1/self.MOUSE_SMOOTHNESS)


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