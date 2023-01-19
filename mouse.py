from screeninfo import get_monitors
import pyautogui


class Mouse:
    def __init__(self):
        self.screen_size = self.get_screen_size()
        

    def move_mouse(self, x:int, y:int):
        pyautogui.moveTo(x * self.screen_size[0], y * self.screen_size[1], 0.5)


    def get_screen_size(self, width_is_fixed:bool = False):
        w, h = 0, 0

        for monitor in get_monitors():
            if width_is_fixed:
                w = monitor.width
                h += monitor.height
            else:
                w += monitor.width
                h = monitor.height

        return (w, h)