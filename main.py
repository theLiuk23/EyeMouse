from eyes import Eyes
import mouse
import cv2
import time, sys


FPS = 60
MOUSE_SMOOTHNESS = 60
webcam = cv2.VideoCapture(0)
eyes = Eyes()
my_mouse = mouse.Mouse(MOUSE_SMOOTHNESS)


while True:
    _, frame = webcam.read()
    cv2.flip(frame, 1)
    eye_position = eyes.detect_eye(frame)
    # my_mouse.move_mouse(eye_position)    

    cv2.imshow("Test", frame)

    time.sleep(1/FPS)
    if cv2.waitKey(1) == ord('q'):
        break


cv2.destroyAllWindows()
webcam.release()
sys.exit(0)