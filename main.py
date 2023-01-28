from eyes import Eyes
import mouse
import cv2
import time, sys
import math


FPS = 20
MOUSE_SMOOTHNESS = FPS
webcam = cv2.VideoCapture(0)
eyes = Eyes()
my_mouse = mouse.Mouse(MOUSE_SMOOTHNESS)


  
while True:
    _, frame = webcam.read()
    cv2.imshow("Test", frame)
    keypress = cv2.waitKey(1)
    time.sleep(1/FPS)

    if None in [my_mouse.MAX_DISTANCE, my_mouse.MIN_DISTANCE]:
        my_mouse.calibrate(frame)

    distance = eyes.detect_eyes_distance(frame)
    print(f'DISTANCE: {distance}')

    if distance is None:
        continue
    my_mouse.move_mouse(distance)

    if keypress == ord('q'):
        break


cv2.destroyAllWindows()
webcam.release()
sys.exit(0)